from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from scripts_data import OTHER_SCRIPTS, ENGAGEMENT_SCRIPTS, VIRAL_PLUG_SCRIPTS


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Visual Style Model
class VisualStyle(BaseModel):
    id: str
    title: str
    images: List[str]
    info: Optional[str] = None

# Hook Model  
class Hook(BaseModel):
    id: str
    category: str
    rank: Optional[int] = None
    idea: str
    reference_links: Optional[str] = None
    notes: Optional[str] = None

# Script Model
class Script(BaseModel):
    id: str
    type: str  # "other" or "engagement"
    rank: Optional[int] = None
    paragraph1: str
    paragraph2: str
    notes: Optional[str] = None

# Dummy Data
VISUAL_STYLES = [
    # Tier 0
    VisualStyle(
        id="vs1",
        title="White Title + White Paragraph:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1207.jpg&x=3600&y=2338&a=true"
        ],
        info="Whenever you're using the stroke text instead of the white background text, you need to make sure your images are suitable for that style.\nIt's important that the text is easily readable, so you should only use images where there's a plain area with not too much going on and place the stroke text directly on that area."
    ),
    VisualStyle(
        id="vs2",
        title="White Title + Stroke Paragraph:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1208.jpg&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs3",
        title="Different emojis after each title:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1213.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1214.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs4",
        title="Numbering Style (:)",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1219.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1220.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    # Tier 1
    VisualStyle(
        id="vs5",
        title="Colored Title + White Paragraph",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1209.PNG&x=3600&y=2338&a=true"
        ],
        info="you can try other colors than pink too just make sure you're not switching colors in the same slideshow"
    ),
    VisualStyle(
        id="vs6",
        title="Same emoji after each title:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1211.jpg&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1212.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs7",
        title="Apple Notes App Style",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1223.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1224.PNG&x=3600&y=2338&a=true"
        ],
        info="usually this format is just 2 slides, hook + screenshot of list taken in apple notes app"
    ),
    # Tier 2
    VisualStyle(
        id="vs8",
        title="Stroke Title + White Paragraph:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1210.jpg&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs9",
        title="Numbering Style (-)",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1217.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1218.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs10",
        title="Numbering Style (Emoji)",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1221.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1222.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    # Tier 3 (Mistakes)
    VisualStyle(
        id="vs11",
        title="Mistakes with red title:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1225.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1226.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    ),
    VisualStyle(
        id="vs12",
        title="Mistakes with X-Emoji:",
        images=[
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1225.PNG&x=3600&y=2338&a=true",
            "https://nx73752.your-storageshare.de/apps/files_sharing/publicpreview/eWkEmENrtSXdG68?file=/IMG_1227.PNG&x=3600&y=2338&a=true"
        ],
        info=None
    )
]

HOOKS = [
    # === REGULAR HOOKS (for non-Mistake styles) ===
    
    # Ex TikTok Category
    Hook(id="h1", category="Ex TikTok", idea="i helped train new hires at tiktok, this is how we explained the algorithm to them…", reference_links="-", notes=None),
    Hook(id="h2", category="Ex TikTok", idea="my seat neighbor on a flight turned out to be a tiktok employee and she spilled tea the whole trip...", reference_links="-", notes=None),
    Hook(id="h3", category="Ex TikTok", idea="my abusive ex worked at tiktok and he told me all the things creators arent supposed to know…", reference_links="-", notes=None),
    Hook(id="h4", category="Ex TikTok", idea="my dad got fired drom tiktok because of who he voted for, now hes spilling the tea…", reference_links="-", notes=None),
    Hook(id="h5", category="Ex TikTok", idea="i just got fired from tiktok for being pregnant, so now im spilling the tea...", reference_links="-", notes=None),
    Hook(id="h6", category="Ex TikTok", idea="i just ran into a tiktok manager at a creator networking event, the advice she gave me was nothing like what's online...", reference_links="-", notes=None),
    Hook(id="h7", category="Ex TikTok", idea="i used to think the tiktok algorithm was random until my dad (who literally built it) told me this...", reference_links="-", notes=None),
    Hook(id="h8", category="Ex TikTok", idea="my dad was part of the team who developed the tiktok fyp algorithm, heres what he revealed…", reference_links="-", notes=None),
    Hook(id="h9", category="Ex TikTok", idea="i ran into a tiktok employee at the airport, and the tea he spilled after 3 drinks was insane…", reference_links="-", notes=None),
    Hook(id="h10", category="Ex TikTok", idea="i used to be in a private tiktok creator group run by employees, heres what they hide about the algorithm...", reference_links="-", notes=None),
    Hook(id="h11", category="Ex TikTok", idea="i used to work in tiktoks creator ops team, and this is what shocked me about the algorithm…", reference_links="-", notes=None),
    Hook(id="h12", category="Ex TikTok", idea="i accidentally got invited to a tiktok staff zoom call (i stayed on mute and took notes)", reference_links="-", notes=None),
    Hook(id="h13", category="Ex TikTok", idea="my uber driver casually mentioned he used to work at tiktok, and the advice he gave me was actually genius…", reference_links="-", notes=None),
    Hook(id="h14", category="Ex TikTok", idea="my dad is the 2nd highest paid tiktok employee, yet no one believes him when he says these things…", reference_links="-", notes=None),
    Hook(id="h15", category="Ex TikTok", idea="my sister worked at tiktok for 4 years and literally quit because of how manipulative the algorithm is…", reference_links="-", notes=None),
    Hook(id="h16", category="Ex TikTok", idea="my sister just dumped her situationship who worked at tiktok, the tea he spilled was insane…", reference_links="-", notes=None),
    Hook(id="h17", category="Ex TikTok", idea="my sister just introduced me to her new bf whos at tiktok and the tea he spilled had my jaw on the floor...", reference_links="-", notes=None),
    Hook(id="h18", category="Ex TikTok", idea="my roommate got fired from tiktok for leaking info, now im sharing the screenshots…", reference_links="-", notes="might be a good hook for the apple notes presentation style"),
    Hook(id="h19", category="Ex TikTok", idea="my situationship casually mentioned he was a tiktok intern and i made him spill the secrets after a few drinks...", reference_links="-", notes=None),
    Hook(id="h20", category="Ex TikTok", idea="my roommate works at tiktok and accidentally left her laptop open, heres what i saw…", reference_links="-", notes=None),
    Hook(id="h21", category="Ex TikTok", idea="my roommate got fired from tiktok for leaking info, guess who has the screenshots…", reference_links="-", notes=None),
    Hook(id="h22", category="Ex TikTok", idea="my college roommate interned at tiktok and now shes sharing all the secrets they told her during training…", reference_links="-", notes=None),
    Hook(id="h23", category="Ex TikTok", idea="my friend accidentally got added to an internal tiktok slack channel and we took screenshots…", reference_links="-", notes=None),
    Hook(id="h24", category="Ex TikTok", idea="i met a tiktok employee at a house party, heres what he told me about the algorithm…", reference_links="-", notes=None),
    Hook(id="h25", category="Ex TikTok", idea="i matched with a tiktok employee on bumble and literally turned the date into an algorithm interview...", reference_links="-", notes=None),
    Hook(id="h26", category="Ex TikTok", idea="i interviewed my boss during my tiktok internship, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="h27", category="Ex TikTok", idea="i overheard two tiktok employees talking at a cafe, heres what they said about low views…", reference_links="-", notes=None),
    Hook(id="h28", category="Ex TikTok", idea="i worked with tiktoks creator training team, and this is what they hide about the algorithm…", reference_links="-", notes=None),
    Hook(id="h29", category="Ex TikTok", idea="if you think the tiktok algorithm is crazy, you're right (i worked at tiktok for 4 years)", reference_links="-", notes=None),
    Hook(id="h30", category="Ex TikTok", idea="the girl next to me on my flight works at tiktok and i made her spill the tea…", reference_links="-", notes=None),
    Hook(id="h31", category="Ex TikTok", idea="i went on a hinge date with a guy who works at tiktok and the things he told me about the algorithm shocked me...", reference_links="-", notes=None),
    Hook(id="h32", category="Ex TikTok", idea="the woman i sat next to on a plane worked at tiktok for 4 years, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="h33", category="Ex TikTok", idea="my dad used to work at tiktok and now hes exposing everything they hide about the algorithm…", reference_links="-", notes=None),
    Hook(id="h34", category="Ex TikTok", idea="my dad just got fired from tiktok after 4 years, so now hes spilling all the tea...", reference_links="https://www.tiktok.com/@emily.growth/photo/7536956508358135062", notes=None),
    Hook(id="h35", category="Ex TikTok", idea="i was a tiktok intern for 5 months until i \"accidentally\" spilled the tea about the algorithm…", reference_links="-", notes=None),
    Hook(id="h36", category="Ex TikTok", idea="my old boss at tiktok slid into my dms last week, here's the tea he spilled after 3 drinks…", reference_links="-", notes=None),
    Hook(id="h37", category="Ex TikTok", idea="i studied accounts of 20 tiktok employees, heres what they do differently…", reference_links="-", notes=None),
    Hook(id="h38", category="Ex TikTok", idea="my dad worked at tiktok for 4 years, yet no one believes him when he says these things...", reference_links="https://www.tiktok.com/@emily.growth/photo/7541441656722050326", notes=None),
    Hook(id="h39", category="Ex TikTok", idea="ive been a tiktok contractor for 4 years, heres the truth about the algorithm…", reference_links="-", notes=None),
    Hook(id="h40", category="Ex TikTok", idea="i just quit my job at tiktok, heres everything they don't want creators to know…", reference_links="-", notes=None),
    Hook(id="h41", category="Ex TikTok", idea="i got laid off from tiktok last month, now im finally spilling what they keep hidden…", reference_links="-", notes=None),
    Hook(id="h42", category="Ex TikTok", idea="i dated a tiktok employee to grow my account, now im spilling the tea…", reference_links="-", notes=None),
    Hook(id="h43", category="Ex TikTok", idea="i got fired from tiktok last month, heres what i can finally say now…", reference_links="-", notes=None),
    Hook(id="h44", category="Ex TikTok", idea="i just quit working at tiktok after 4 years, heres everything i wasn't supposed to tell you…", reference_links="-", notes=None),
    Hook(id="h45", category="Ex TikTok", idea="my toxic ex interned at tiktok for 5 months and now im exposing everything he told me…", reference_links="-", notes=None),
    Hook(id="h46", category="Ex TikTok", idea="tiktok just fired me for what i posted on my private account, so now im spilling all the tea…", reference_links="-", notes=None),
    Hook(id="h47", category="Ex TikTok", idea="i just went on a tinder date with a guy who works at tiktok, heres what he told me after 3 drinks...", reference_links="-", notes=None),
    Hook(id="h48", category="Ex TikTok", idea="what i learned about the algorithm as a tiktok intern…", reference_links="-", notes=None),
    Hook(id="h49", category="Ex TikTok", idea="my college roommate was a tiktok intern this summer and what they hide about the algorithm is crazy…", reference_links="-", notes=None),
    Hook(id="h50", category="Ex TikTok", idea="i just got fired from tiktok after 4 years, heres everything they hide about the algorithm...", reference_links="https://www.tiktok.com/@ava.goviral/photo/7533635223213427990", notes=None),
    Hook(id="h51", category="Ex TikTok", idea="ive been a tiktok intern for 5 months, heres what shocked me about the algorithm...", reference_links="https://www.tiktok.com/@emily.growth/photo/7528079925551648022", notes=None),
    Hook(id="h52", category="Ex TikTok", idea="i just got fired from tiktok after 4 years, so now im spilling all the tea...", reference_links="https://www.tiktok.com/@emily.growth/photo/7526219405135547670", notes=None),
    Hook(id="h53", category="Ex TikTok", idea="5 things i do every day as a tiktok intern to grow my account…", reference_links="-", notes=None),
    Hook(id="h54", category="Ex TikTok", idea="the wildest things ive learned about the algorithm during my internship at tiktok...", reference_links="-", notes=None),

    # Professor Category
    Hook(id="p1", category="Professor", idea="my dad is a harvard professor who worked on tiktoks recommendation algorithm, heres what he revealed…", reference_links="-", notes=None),
    Hook(id="p2", category="Professor", idea="my dad is a harvard marketing professor, and heres the tiktok advice his students pay thousands for…", reference_links="-", notes=None),
    Hook(id="p3", category="Professor", idea="my harvard marketing professor just broke down the tiktok algorithm in class, and heres what shocked me…", reference_links="-", notes=None),
    Hook(id="p4", category="Professor", idea="my dad teaches social media at harvard, and his students pay $50k a year to hear what im about to tell you for free…", reference_links="-", notes=None),
    Hook(id="p5", category="Professor", idea="my harvard professor gave us a private lecture on the tiktok algorithm, and heres what shocked everyone…", reference_links="-", notes=None),
    Hook(id="p6", category="Professor", idea="my harvard marketing professor did a lecture about the tiktok algorithm, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="p7", category="Professor", idea="my marketing professor consults for fortune 500 brands, and heres the tiktok advice he gave us…", reference_links="-", notes=None),
    Hook(id="p8", category="Professor", idea="my dad teaches social media strategy at harvard, and his advice about growing on tiktok blew my mind…", reference_links="-", notes=None),
    Hook(id="p9", category="Professor", idea="my harvard marketing professor is the 2nd highest paid in the world, and heres the tiktok advice his students pay $80k a year for…", reference_links="-", notes=None),
    Hook(id="p10", category="Professor", idea="my professor who also works at tiktok gave us advice about the algorithm…", reference_links="-", notes=None),
    Hook(id="p11", category="Professor", idea="i worked at a social media agency managing creators with 1M followers, and this is the advice we gave clients behind closed doors…", reference_links="-", notes=None),
    Hook(id="p12", category="Professor", idea="ive been hearing a lecture from a harvard social media professor about tiktok, and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="p13", category="Professor", idea="my university invited a guest lecturer from tiktok, heres what ive learned about the algo…", reference_links="-", notes=None),

    # Official TikTok Category
    Hook(id="o1", category="Official TikTok", idea="i got invited to a private tiktok creator dinner, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="o2", category="Official TikTok", idea="i was one of five creators that got invited to visit tiktoks HQ, heres what shocked me...", reference_links="-", notes=None),
    Hook(id="o3", category="Official TikTok", idea="i went through a brand partnership training with tiktok, heres what shocked me about the algorithm…", reference_links="-", notes=None),
    Hook(id="o4", category="Official TikTok", idea="i went to a happy hour full of tiktok staff, here's what they told me after two drinks…", reference_links="-", notes=None),
    Hook(id="o5", category="Official TikTok", idea="i joined a private workshop with creators over 1M followers, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="o6", category="Official TikTok", idea="i went through tiktoks official creator training, heres the checklist they gave us…", reference_links="-", notes=None),
    Hook(id="o7", category="Official TikTok", idea="i was invited to a tiktok roundtable for creators, heres what they revealed…", reference_links="-", notes=None),
    Hook(id="o8", category="Official TikTok", idea="tiktok flew me out for a private creator workshop, heres what shocked me…", reference_links="-", notes=None),
    Hook(id="o9", category="Official TikTok", idea="i went to a secret tiktok creator workshop, heres what they revealed about the algorithm…", reference_links="-", notes=None),
    Hook(id="o10", category="Official TikTok", idea="i went through tiktoks creator bootcamp and heres what blew my mind…", reference_links="-", notes=None),
    Hook(id="o11", category="Official TikTok", idea="i interviewed 5 tiktok employees at an official event, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="o12", category="Official TikTok", idea="i got invited to the official tiktok creator summit, heres what ive learned...", reference_links="-", notes=None),
    Hook(id="o13", category="Official TikTok", idea="i got invited to visit tiktoks headquarters, heres everything they revealed about the algorithm...", reference_links="https://www.tiktok.com/@emily.growth/photo/7529567581452242198", notes=None),
    Hook(id="o14", category="Official TikTok", idea="i got invited to an official tiktok creator event, heres what ive learned...", reference_links="https://www.tiktok.com/@growth_sarah/photo/7532542490734284040", notes=None),
    Hook(id="o15", category="Official TikTok", idea="i went through tiktoks official creator training, heres what ive learned...", reference_links="https://www.tiktok.com/@madisonfromnyy/photo/7524515127320759607", notes=None),

    # Experienced Category
    Hook(id="e1", category="Experienced", idea="my manager used to rep creators with millions, and the growth strategies they told me to use were insane…", reference_links="-", notes=None),
    Hook(id="e2", category="Experienced", idea="i am the 2nd highest paid tiktok creator in my country, heres what ive learned...", reference_links="-", notes=None),
    Hook(id="e3", category="Experienced", idea="i ran tiktok ads for government campaigns and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e4", category="Experienced", idea="i used to manage social media for netflix and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e5", category="Experienced", idea="i used to work on duolingos tiktok team, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e6", category="Experienced", idea="my manager manages 10 creators with over 1M followers, and heres what they do differently…", reference_links="-", notes=None),
    Hook(id="e7", category="Experienced", idea="i studied the tiktok algorithm for my thesis at harvard and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e8", category="Experienced", idea="i got into a private group chat with 50 creators over 1M followers, heres what they do differently…", reference_links="-", notes=None),
    Hook(id="e9", category="Experienced", idea="heres how i went from 300 to 45k followers in 3 months…", reference_links="-", notes=None),
    Hook(id="e10", category="Experienced", idea="my sister is the second biggest creator in her country, yet no one believes her when she says these things...", reference_links="https://www.tiktok.com/@emily.growth/photo/7538430990054690070", notes=None),
    Hook(id="e11", category="Experienced", idea="i studied the tiktok algorithm as part of my social media phd, heres what shocked me…", reference_links="-", notes=None),
    Hook(id="e12", category="Experienced", idea="i asked 10 creators with over 1M followers what they regret doing in their first 6 months, here's what they said…", reference_links="-", notes=None),
    Hook(id="e13", category="Experienced", idea="i used to manage creators for a social media agency, heres what i wish every small creator knew…", reference_links="-", notes=None),
    Hook(id="e14", category="Experienced", idea="i used to work at a marketing agency partnered with tiktok, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e15", category="Experienced", idea="after growing 5 pages to over 100k, heres what small creators get wrong…", reference_links="-", notes=None),
    Hook(id="e16", category="Experienced", idea="ive been watching my bf grow his account to 800k, and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e17", category="Experienced", idea="what i know about the algorithm as a qualified social media manager…", reference_links="-", notes=None),
    Hook(id="e18", category="Experienced", idea="my sister worked in PR for 4 years, here's how they make creators blow up on tiktok…", reference_links="-", notes=None),
    Hook(id="e19", category="Experienced", idea="my sister just hit 1M followers, yet no one believes her when she says these things…", reference_links="-", notes=None),
    Hook(id="e20", category="Experienced", idea="i studied the last 100 videos from the top 10 fastest growing creators, heres the pattern they all use…", reference_links="-", notes=None),
    Hook(id="e21", category="Experienced", idea="tiktok has a hidden scoring system for creators, and i figured out how it works…", reference_links="-", notes=None),
    Hook(id="e22", category="Experienced", idea="i literally copied the strategy of a creator with 1M followers for 30 days, heres what ive learned…", reference_links="-", notes=None),
    Hook(id="e23", category="Experienced", idea="tips for small creators trying to grow on tiktok…", reference_links="-", notes=None),

    # Journalist Category
    Hook(id="j1", category="Journalist", idea="i sat next to the tiktok ceo on my flight and made him spill some tea...", reference_links="-", notes=None),
    Hook(id="j2", category="Journalist", idea="i interviewed the tiktok ceo about the algorithm and heres what shocked me…", reference_links="-", notes=None),
    Hook(id="j3", category="Journalist", idea="i studied the 50 biggest creators in my country and heres what they all have in common…", reference_links="-", notes=None),
    Hook(id="j4", category="Journalist", idea="i read through every patent tiktok has filed, and heres what shocked me about the algorithm…", reference_links="-", notes=None),

    # New TikTok Algorithm Category
    Hook(id="n1", category="New TikTok Algorithm", idea="the US TikTok split just changed everything and heres how to blow up right now…", reference_links="-", notes=None),
    Hook(id="n2", category="New TikTok Algorithm", idea="the new tiktok us only app is basically a reset button and heres how you can take advantage…", reference_links="-", notes=None),
    Hook(id="n3", category="New TikTok Algorithm", idea="the new tiktok us only app is your chance to blow up and heres how…", reference_links="-", notes=None),
    Hook(id="n4", category="New TikTok Algorithm", idea="i studied everything about the new TikTok US only app, heres what small creators need to know…", reference_links="-", notes=None),
    Hook(id="n5", category="New TikTok Algorithm", idea="how to take advantage of the new tiktok us only app before everyone else does...", reference_links="-", notes=None),
    Hook(id="n6", category="New TikTok Algorithm", idea="why the new tiktok us only app is the best thing that ever happened to small creators…", reference_links="-", notes=None),

    # Learnings Category
    Hook(id="l1", category="Learnings", idea="my signature way to post consistently while working a full time job…", reference_links="-", notes=None),
    Hook(id="l2", category="Learnings", idea="i regret posting consistently and heres why i would never do it again…", reference_links="-", notes=None),
    Hook(id="l3", category="Learnings", idea="i tried posting consistently for 30 days and heres what happened…", reference_links="-", notes=None),
    Hook(id="l4", category="Learnings", idea="i posted one tiktok everyday since january and heres what ive learned...", reference_links="https://www.tiktok.com/@emily.growth/photo/7516156465493658902", notes=None),
    Hook(id="l5", category="Learnings", idea="i posted every day for 100 days and heres what ive learned…", reference_links="-", notes=None),
    Hook(id="l6", category="Learnings", idea="i forced myself to post every time i opened tiktok, heres what happened...", reference_links="https://www.tiktok.com/@madisonfromnyy/photo/7524879967235231031", notes=None),
    Hook(id="l7", category="Learnings", idea="5 harsh truths that finally made me grow my account...", reference_links="https://www.tiktok.com/@emily.growth/photo/7542187564682317078", notes=None),
    Hook(id="l8", category="Learnings", idea="ive been posting consistently for 5 months, heres what ive learned...", reference_links="https://www.tiktok.com/@emily.growth/photo/7502390436095347990", notes=None),
    Hook(id="l9", category="Learnings", idea="the biggest lessons i learned from posting consistently…", reference_links="-", notes=None),
    Hook(id="l10", category="Learnings", idea="i tried every single tiktok growth strategy, heres what actually worked...", reference_links="-", notes=None),

    # AI Tips Category
    Hook(id="a1", category="AI Tips", idea="i made chatgpt spill all the tea about the tiktok algorithm, heres what they hide…", reference_links="-", notes=None),

    # === MISTAKE HOOKS (for Mistake styles only) ===
    Hook(id="m1", category="Ex TikTok - Mistakes", idea="i just interviewed an ex tiktok engineer, here are the biggest mistakes small creators make....", reference_links="-", notes=None),
    Hook(id="m2", category="Professor - Mistakes", idea="my mom teaches social media studies at harvard, here are common mistakes creators make on tiktok…", reference_links="-", notes=None),
    Hook(id="m3", category="Official TikTok - Mistakes", idea="i attended a tiktok strategy session for verified creators and heres what small creators are doing wrong…", reference_links="-", notes=None),
    Hook(id="m4", category="Experienced - Mistakes", idea="ive been coaching creators for 4 years and 90% of them were making the same mistakes…", reference_links="-", notes=None),
    Hook(id="m5", category="Learnings - Mistakes", idea="ive been posting consistently for 5 months now, here are my biggest red flags…", reference_links="-", notes=None),
    Hook(id="m6", category="Learnings - Mistakes", idea="common mistakes i see small creators make on tiktok...", reference_links="-", notes=None)
]

SCRIPTS = [
    # Viral Plug Scripts (for Script 4)
    Script(
        id="vp1", type="viral_plug", rank=None,
        paragraph1="not using tools that help",
        paragraph2="before i quit, i found this app called Go Viral. it uses the same kind of retention and hook testing we used internally. it predicts how your video will do and literally tells you what to fix. i swear it's spooky accurate, and it's the only reason i'd feel confident posting daily now 🤯💗",
        notes=None
    ),
    Script(
        id="vp2", type="viral_plug", rank=None,
        paragraph1="not using the right tools.",
        paragraph2="for so long i thought i had to figure it all out on my own. then i found the go viral app that shows you how to improve your video before you post. pacing, captions and all that. i wish i had it sooner. feels like a little algorithm bff💗",
        notes=None
    ),
    Script(
        id="vp3", type="viral_plug", rank=None,
        paragraph1="not testing your content first.",
        paragraph2="this is my biggest cheat code. i use the go viral app to check my vids before posting. it predicts performance and shows what to tweak. it's giving algorithm whisperer 💗🧡",
        notes=None
    ),
    Script(
        id="vp4", type="viral_plug", rank=None,
        paragraph1="only guessing what's wrong.",
        paragraph2="this is a big one. people keep guessing why they're not growing. i use the go viral app that literally tells me what's off before i post. it's like a little algorithm bff 🧡💗",
        notes=None
    ),
    Script(
        id="vp5", type="viral_plug", rank=None,
        paragraph1="not testing your content first.",
        paragraph2="this is my biggest cheat code. i use the go viral app to check my vids before posting. it predicts performance and shows what to tweak. it's giving algorithm whisperer 💗🧡",
        notes=None
    ),
    Script(
        id="vp6", type="viral_plug", rank=None,
        paragraph1="improve before i even post.",
        paragraph2="feels like a little algorithm bff 💗",
        notes=None
    ),
    
    # Other Scripts
    Script(
        id="s1", type="other", rank=None,
        paragraph1="not reusing what worked.",
        paragraph2="if something did well, do it again. same topic, new angle. viral creators repeat themselves all the time. that's not lazy, that's smart 💡",
        notes=None
    ),
    Script(
        id="s2", type="other", rank=None,
        paragraph1="quitting right before it clicks.",
        paragraph2="there were weeks i almost gave up. i thought i wasn't cut out for this. but i kept showing up. and one random post changed everything. don't leave right before it gets good 🌟",
        notes=None
    ),
    Script(
        id="s3", type="other", rank=None,
        paragraph1="making content for the algorithm.",
        paragraph2="the algorithm follows attention. attention follows connection. make it for the people, not the robots. it works way better that way 💗",
        notes=None
    ),
    Script(
        id="s4", type="other", rank=None,
        paragraph1='not "training" the algorithm properly.',
        paragraph2='your first 5-10 posts are teaching the system who you are. if you keep switching niches, it gets confused. we used to call it "identity scrambling" internally. the fastest growth always came from predictable, clear content patterns 📊🌟',
        notes=None
    ),
    Script(
        id="s5", type="other", rank=None,
        paragraph1="posting like the algorithm is your enemy.",
        paragraph2='when i worked at tiktok, i saw this all the time. creators would panic after one bad post, switch niches, delete videos. the system reads that as "inconsistent" and literally stops testing your content as much. the creators who stayed calm? their reach always bounced back 💪',
        notes=None
    ),
    Script(
        id="s6", type="other", rank=None,
        paragraph1="deleting videos too soon.",
        paragraph2="i'd post something, check after 30 mins, and delete if it flopped. but the algorithm moves slow sometimes. one of my best posts sat at 100 views for hours... then hit 100k overnight 💫",
        notes=None
    ),
    Script(
        id="s7", type="other", rank=None,
        paragraph1='deleting "flops" too fast.',
        paragraph2="just because it didn't pop off in the first hour doesn't mean it won't. tiktok loves to pick up older vids. give it time babe, your moment might just be delayed 🌸💜",
        notes=None
    ),
    Script(
        id="s8", type="other", rank=None,
        paragraph1="being \"too niche\" too soon.",
        paragraph2="niching down too early can box you in. if you're still growing, test different vibes. find what actually sticks before locking in 💚",
        notes=None
    ),
    Script(
        id="s9", type="other", rank=None,
        paragraph1="quitting too soon.",
        paragraph2="growth doesn't always show right away. that doesn't mean it's not happening. most people stop right before it clicks. don't let that be you 🌸💜",
        notes=None
    ),
    Script(
        id="s10", type="other", rank=None,
        paragraph1="trying to be perfect instead of consistent.",
        paragraph2="you don't need a ring light or the best mic. you just need to show up. done is better than perfect, always 💡",
        notes=None
    ),
    Script(
        id="s11", type="other", rank=None,
        paragraph1="forgetting how far you've come.",
        paragraph2="you might not be where you wanna be yet. but you're not where you started either. that progress? that's real. don't quit on your almost 🌟💜",
        notes=None
    ),
    Script(
        id="s12", type="other", rank=None,
        paragraph1="cringing at your own posts.",
        paragraph2="everyone starts there. it's part of the process. consistency makes you fearless. the more you post, the less you care and the more your confidence grows 🙌",
        notes=None
    ),
    Script(
        id="s13", type="other", rank=None,
        paragraph1="believing you're shadowbanned.",
        paragraph2="most of the time? you're not. your vid just didn't hit. don't spiral. learn from it, adjust, and post again. the next one could be the beginning of a new chapter",
        notes=None
    ),
    Script(
        id="s14", type="other", rank=None,
        paragraph1="posting just to post.",
        paragraph2="like no hook, no story, no structure... just vibes i get it, consistency matters. but if you're not giving people a reason to stay, you're just adding noise...",
        notes=None
    ),
    Script(
        id="s15", type="other", rank=None,
        paragraph1="being scared to repeat themself.",
        paragraph2="i used to think i had to come up with something new every day. but the posts that worked? i repeated them. same topic, same format, sometimes even the same hook. and they still did well 🙌",
        notes=None
    ),
    Script(
        id="s16", type="other", rank=None,
        paragraph1="being a silent scroller.",
        paragraph2="the moment i started interacting for real, my page got more love too. the algorithm sees it, and so do the people. give what you're hoping to receive 🧡",
        notes=None
    ),
    Script(
        id="s17", type="other", rank=None,
        paragraph1="thinking you're too late.",
        paragraph2="you're not late. you're not shadowbanned. you're learning. tiktok rewards the ones who stick around. keep showing up. your moment's coming 💗",
        notes=None
    ),
    
    # Engagement Trigger Scripts
    Script(
        id="e1", type="engagement", rank=None,
        paragraph1="not cheering for your own people.",
        paragraph2="this is still a team sport. comment on your mutuals. share their stuff. tag them. building together is always faster than growing alone 🤝",
        notes=None
    ),
    Script(
        id="e2", type="engagement", rank=None,
        paragraph1="not treating it like a team sport.",
        paragraph2="this isn't a solo game. hyping others up boosts you too. tiktok notices when you're active in the community. support your mutuals, reply, comment. it all adds up ⚡",
        notes=None
    ),
    Script(
        id="e3", type="engagement", rank=None,
        paragraph1="being a silent scroller.",
        paragraph2="the moment i started interacting for real, my page got more love too. the algorithm sees it, and so do the people. give what you're hoping to receive 🤝",
        notes=None
    ),
    Script(
        id="e4", type="engagement", rank=None,
        paragraph1="not engaging the way the app wants you to.",
        paragraph2='this is the most underrated secret. if you only post but never genuinely comment, like, or watch other videos, the system thinks you\'re not part of the community. i used to watch internal dashboards track this in real time. creators who acted like "viewers" got pushed like crazy 👀⚡',
        notes=None
    ),
    Script(
        id="e5", type="engagement", rank=None,
        paragraph1="forgetting to support others.",
        paragraph2="if you post and then dip without engaging, you're missing out. tiktok is social for a reason. comment, share, hype your mutuals. the algorithm loves it when you're active 🤝",
        notes=None
    ),
    Script(
        id="e6", type="engagement", rank=None,
        paragraph1="being a silent scroller.",
        paragraph2="the moment i started interacting for real, my page got more love too, and so do the people. give what you're hoping to receive 🤗",
        notes=None
    )
]

# API Routes
@api_router.get("/")
async def root():
    return {"message": "She's Viral API"}

@api_router.get("/visual-styles", response_model=List[VisualStyle])
async def get_visual_styles():
    return VISUAL_STYLES

@api_router.get("/hooks", response_model=List[Hook])
async def get_hooks():
    return HOOKS

@api_router.get("/hooks/{category}", response_model=List[Hook])
async def get_hooks_by_category(category: str):
    return [h for h in HOOKS if h.category.lower().replace(" ", "-") == category.lower()]

@api_router.get("/scripts", response_model=List[Script])
async def get_scripts():
    # Build scripts from external data
    all_scripts = []
    
    # Other Scripts
    for idx, s in enumerate(OTHER_SCRIPTS):
        all_scripts.append(Script(
            id=f"s{idx+1}",
            type="other",
            paragraph1=s["paragraph1"],
            paragraph2=s["paragraph2"],
            notes=None
        ))
    
    # Engagement Scripts
    for idx, s in enumerate(ENGAGEMENT_SCRIPTS):
        all_scripts.append(Script(
            id=f"e{idx+1}",
            type="engagement",
            paragraph1=s["paragraph1"],
            paragraph2=s["paragraph2"],
            notes=None
        ))
    
    # Viral Plug Scripts
    for idx, s in enumerate(VIRAL_PLUG_SCRIPTS):
        all_scripts.append(Script(
            id=f"vp{idx+1}",
            type="viral_plug",
            paragraph1=s["paragraph1"],
            paragraph2=s["paragraph2"],
            notes=None
        ))
    
    return all_scripts

@api_router.get("/scripts/{script_type}", response_model=List[Script])
async def get_scripts_by_type(script_type: str):
    all_scripts = await get_scripts()
    return [s for s in all_scripts if s.type == script_type]

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
