import random
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

# --- Data Models ---

class Player:
    def __init__(self, name: str):
        self.name = name
        self.team = None       # "straight" or "gay"
        self.position = None   # "king" or "normal"

class Room:
    def __init__(self, room_id: int, creator_name: str):
        self.room_id = room_id
        self.creator_name = creator_name
        self.players: dict[str, Player] = {}  # keyed by lowercase name
        self.state = "lobby"   # "lobby" or "playing"
        self.num_gay = 0
        self.party_size = 4

# --- In-Memory Storage ---

rooms: dict[int, Room] = {}

# --- Card Prompts ---

CARD_PROMPTS = [
    "Select a player. They must show their team to one of the players directly next to them.",
    "Select a player. They must show their team to one of the players directly next to them.",
    "Select a player. They must show their team card to you.",
    "Select a player. They must show their team card to you.",
    "Reveal the discarded cards from the last round.",
    "Pick the next host.",
    "Pick two players. They must show each other their team cards.",
]

# --- Request Models ---

class CreateRoomRequest(BaseModel):
    player_name: str

class JoinRoomRequest(BaseModel):
    room_id: int
    player_name: str

class StartGameRequest(BaseModel):
    room_id: int
    player_name: str
    num_gay: int
    party_size: int

# --- Helpers ---

def generate_room_id() -> int:
    existing = set(rooms.keys())
    for _ in range(100):
        rid = random.randint(1, 1000)
        if rid not in existing:
            return rid
    for rid in range(1, 1001):
        if rid not in existing:
            return rid
    return -1

def get_player(room: Room, name: str):
    return room.players.get(name.lower())

# --- Routes ---

@router.get("/slumberparty")
async def slumberparty_page():
    return FileResponse("pages/slumberparty.html")

@router.get("/slumberparty/room")
async def slumberparty_room_page():
    return FileResponse("pages/slumberparty.html")

@router.post("/slumberparty/api/create-room")
async def create_room(req: CreateRoomRequest):
    name = req.player_name.strip()
    if not name:
        return {"error": "Name is required"}
    rid = generate_room_id()
    if rid == -1:
        return {"error": "No rooms available. Try again later."}
    player = Player(name)
    room = Room(rid, name.lower())
    room.players[name.lower()] = player
    rooms[rid] = room
    return {"room_id": rid}

@router.post("/slumberparty/api/join-room")
async def join_room(req: JoinRoomRequest):
    name = req.player_name.strip()
    if not name:
        return {"error": "Name is required"}
    room = rooms.get(req.room_id)
    if not room:
        return {"error": "Room not found"}
    key = name.lower()
    existing = room.players.get(key)
    if existing:
        # Same name = same player, treat as rejoin
        pass
    elif room.state != "lobby":
        return {"error": "Game already started"}
    else:
        player = Player(name)
        room.players[key] = player

    # Return room state along with join response
    player_names = [p.name for p in room.players.values()]
    count = len(player_names)
    response = {
        "ok": True,
        "state": room.state,
        "players": player_names,
        "is_creator": key == room.creator_name,
        "player_count": count,
    }
    if room.state == "lobby":
        response["suggested_gay"] = max(1, round(count / 3))
        response["suggested_party_size"] = min(count, 4) if count <= 5 else 5
    else:
        response["party_size"] = room.party_size
    return response

@router.get("/slumberparty/api/room-state")
async def room_state(room_id: int, player_name: str):
    room = rooms.get(room_id)
    if not room:
        return {"error": "Room not found"}
    player = get_player(room, player_name)
    if not player:
        return {"error": "Player not found in room"}
    player_names = [p.name for p in room.players.values()]
    count = len(player_names)
    suggested_gay = max(1, round(count / 3))
    suggested_party = min(count, 4) if count <= 5 else 5

    if room.state == "lobby":
        return {
            "state": "lobby",
            "players": player_names,
            "is_creator": player_name.lower() == room.creator_name,
            "player_count": count,
            "suggested_gay": suggested_gay,
            "suggested_party_size": suggested_party,
        }
    else:
        return {
            "state": "playing",
            "players": player_names,
            "party_size": room.party_size,
        }

@router.post("/slumberparty/api/start-game")
async def start_game(req: StartGameRequest):
    room = rooms.get(req.room_id)
    if not room:
        return {"error": "Room not found"}
    if req.player_name.lower() != room.creator_name:
        return {"error": "Only the room creator can start the game"}
    if room.state != "lobby":
        return {"error": "Game already started"}
    keys = list(room.players.keys())
    count = len(keys)
    if count < 3:
        return {"error": "Need at least 3 players"}
    if req.num_gay < 1 or req.num_gay >= count:
        return {"error": "Invalid number of gay players"}
    if req.party_size < 2 or req.party_size > count:
        return {"error": "Invalid party size"}

    room.num_gay = req.num_gay
    room.party_size = req.party_size

    random.shuffle(keys)
    gay_keys = set(keys[:req.num_gay])
    straight_keys = set(keys[req.num_gay:])

    for k in gay_keys:
        room.players[k].team = "gay"
        room.players[k].position = "normal"
    for k in straight_keys:
        room.players[k].team = "straight"
        room.players[k].position = "normal"

    room.players[random.choice(list(straight_keys))].position = "king"
    room.players[random.choice(list(gay_keys))].position = "king"

    room.state = "playing"
    return {"success": True}

@router.get("/slumberparty/api/my-info")
async def my_info(room_id: int, player_name: str):
    room = rooms.get(room_id)
    if not room or room.state != "playing":
        return {"error": "Game not active"}
    player = get_player(room, player_name)
    if not player:
        return {"error": "Player not found"}
    return {
        "team": player.team,
        "position": player.position,
        "is_gay_king": player.team == "gay" and player.position == "king",
    }

@router.get("/slumberparty/api/my-knowledge")
async def my_knowledge(room_id: int, player_name: str):
    room = rooms.get(room_id)
    if not room or room.state != "playing":
        return {"error": "Game not active"}
    player = get_player(room, player_name)
    if not player:
        return {"error": "Player not found"}

    gay_names = [p.name for p in room.players.values() if p.team == "gay"]

    if player.team == "straight" and player.position == "normal":
        return {"knowledge": "no_information", "members": []}
    else:
        return {"knowledge": "gay_members", "members": gay_names}

@router.get("/slumberparty/api/host-party")
async def host_party(room_id: int, player_name: str):
    room = rooms.get(room_id)
    if not room or room.state != "playing":
        return {"error": "Game not active"}
    player = get_player(room, player_name)
    if not player:
        return {"error": "Player not found"}

    party_size = room.party_size
    others = [p.name for p in room.players.values() if p.name.lower() != player_name.lower()]
    random.shuffle(others)
    party = [player.name] + others[:party_size - 1]
    return {"party": party}

@router.get("/slumberparty/api/draw-card")
async def draw_card():
    return {"prompt": random.choice(CARD_PROMPTS)}

@router.get("/slumberparty/api/fake-team")
async def fake_team(room_id: int, player_name: str):
    room = rooms.get(room_id)
    if not room or room.state != "playing":
        return {"error": "Game not active"}
    player = get_player(room, player_name)
    if not player:
        return {"error": "Player not found"}
    if not (player.team == "gay" and player.position == "king"):
        return {"error": "Only the Gay King can use this"}
    return {"fake_team": "Straight"}
