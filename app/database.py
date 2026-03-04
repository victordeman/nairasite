import os
import libsql_client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper to convert libsql ResultSet to list of dicts
def to_dict_list(result_set: libsql_client.ResultSet):
    return [
        {col: row[i] for i, col in enumerate(result_set.columns)}
        for row in result_set.rows
    ]

# Use Turso Database URL and Auth Token from environment variables
# For local development, it defaults to a local file
# On Vercel, if TURSO_DATABASE_URL is not provided, fallback to /tmp/naira.db
if os.getenv("TURSO_DATABASE_URL"):
    DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
elif os.getenv("VERCEL"):
    DATABASE_URL = "file:/tmp/naira.db"
else:
    DATABASE_URL = "file:naira.db"

AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

async def get_db():
    client = libsql_client.create_client(url=DATABASE_URL, auth_token=AUTH_TOKEN)
    try:
        yield client
    finally:
        await client.close()

async def init_db():
    logger.info(f"Initializing database at {DATABASE_URL}...")
    try:
        async with libsql_client.create_client(url=DATABASE_URL, auth_token=AUTH_TOKEN) as client:
            await client.execute("""
                CREATE TABLE IF NOT EXISTS contact_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT '',
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await client.execute("""
                CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await client.execute("""
                CREATE TABLE IF NOT EXISTS pillars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    icon TEXT NOT NULL,
                    color TEXT NOT NULL
                )
            """)
            await client.execute("""
                CREATE TABLE IF NOT EXISTS architecture_layers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    layer_number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    icon TEXT NOT NULL,
                    color TEXT NOT NULL,
                    tags TEXT NOT NULL DEFAULT '[]'
                )
            """)
            await client.execute("""
                CREATE TABLE IF NOT EXISTS revenue_streams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    icon TEXT NOT NULL,
                    color TEXT NOT NULL
                )
            """)
            await client.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    icon TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)

            # Seed pillars if empty
            cursor = await client.execute("SELECT COUNT(*) FROM pillars")
            count = cursor.rows[0][0]
            if count == 0:
                logger.info("Seeding pillars...")
                pillars_data = [
                    ("01", "African-Centered AI Research", "Focus on embedding African languages and indigenous knowledge into AI to create culturally relevant technologies that serve local contexts.", "database", "indigo"),
                    ("02", "Educational Transformation", "Use XR and agentic AI technologies to revolutionize education and automate academic workflows for immersive learning.", "monitor", "amber"),
                    ("03", "Entrepreneurship Empowerment", "Foster a culture of creators and innovators to promote entrepreneurship within academic communities and beyond.", "users", "emerald"),
                    ("04", "Pan-African Innovation Network", "Build collaborative networks between universities and industries across Africa to drive innovation and knowledge sharing.", "share-2", "purple"),
                    ("05", "Sustainable Monetization", "Develop diverse revenue streams and marketplaces for AI and XR solutions to ensure long-term sustainability.", "trending-up", "rose"),
                    ("06", "Accessibility & Scalability", "Ensure solutions are scalable and accessible across devices using cloud-based architectures and modular platforms.", "cloud", "cyan"),
                ]
                await client.batch([
                    ("INSERT INTO pillars (number, title, description, icon, color) VALUES (?, ?, ?, ?, ?)", p)
                    for p in pillars_data
                ])

            # Seed architecture layers if empty
            cursor = await client.execute("SELECT COUNT(*) FROM architecture_layers")
            count = cursor.rows[0][0]
            if count == 0:
                logger.info("Seeding architecture layers...")
                layers_data = [
                    (1, "Experience Layer", "Focuses on immersive and interactive experiences using XR classrooms to provide immersive learning environments with AI-driven interfaces for students and faculty.", "box", "indigo", '["XR Classrooms", "AI Interfaces", "Immersive Learning"]'),
                    (2, "Intelligence Layer", "Integrates Generative AI and Agentic AI to provide intelligent decision-making and adaptive learning capabilities through autonomous educational agents.", "cpu", "amber", '["Generative AI", "Agentic Systems", "Adaptive Learning"]'),
                    (3, "Data & Integration Layer", "Manages data flow and integrates diverse datasets with secure API Gateway and Event Bus enabling interoperability, scalability, and data sovereignty.", "hard-drive", "emerald", '["Secure APIs", "Data Sovereignty", "System Connectivity"]'),
                ]
                await client.batch([
                    ("INSERT INTO architecture_layers (layer_number, title, description, icon, color, tags) VALUES (?, ?, ?, ?, ?, ?)", l)
                    for l in layers_data
                ])

            # Seed revenue streams if empty
            cursor = await client.execute("SELECT COUNT(*) FROM revenue_streams")
            count = cursor.rows[0][0]
            if count == 0:
                logger.info("Seeding revenue streams...")
                revenue_data = [
                    ("XR Modules Marketplace", "Sell XR lessons to schools, corporate partners, and training centers as a core revenue stream, creating a vibrant ecosystem of African-centered educational content.", "package", "purple"),
                    ("Corporate & Government Training", "Offer tailored AI and XR courses for professional development in corporate and government sectors, driving digital transformation across industries.", "briefcase", "blue"),
                    ("Subscription Access", "Provide premium subscriptions granting students and faculty access to advanced simulations and AI agents, ensuring continuous learning and innovation.", "credit-card", "rose"),
                    ("Research Collaboration & Grants", "Engage in joint research projects funded by African and global institutions to drive innovation and establish thought leadership in AI/XR domains.", "award", "cyan"),
                ]
                await client.batch([
                    ("INSERT INTO revenue_streams (title, description, icon, color) VALUES (?, ?, ?, ?)", r)
                    for r in revenue_data
                ])

            # Seed projects if empty
            cursor = await client.execute("SELECT COUNT(*) FROM projects")
            count = cursor.rows[0][0]
            if count == 0:
                logger.info("Seeding projects...")
                projects_data = [
                    ("African Language LLM", "Developing large language models specifically optimized for indigenous African languages to improve accessibility and digital inclusion.", "message-circle", "AI Research", "In Progress"),
                    ("XR Medical Simulation", "An immersive XR platform for medical students in Africa to practice surgical procedures in a safe, virtual environment.", "heart", "XR Education", "Beta"),
                    ("Agentic Academic Assistant", "AI-driven autonomous agents that help university faculty automate administrative tasks and personalize student learning paths.", "user-check", "Agentic AI", "Early Access"),
                    ("Pan-African Tech Network", "A decentralized platform connecting innovators across the continent to share resources and collaborate on high-impact tech projects.", "share-2", "Innovation", "Operational"),
                ]
                await client.batch([
                    ("INSERT INTO projects (title, description, icon, category, status) VALUES (?, ?, ?, ?, ?)", p)
                    for p in projects_data
                ])
        logger.info("Database initialization successful.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # In production we might not want to re-raise, but for debugging Vercel it's better to see the crash
        raise e
