import aiosqlite
import os

# On Vercel, the only writable directory is /tmp
if os.getenv("VERCEL"):
    DATABASE_PATH = "/tmp/naira.db"
else:
    DATABASE_PATH = os.getenv("DATABASE_PATH", "naira.db")

async def get_db():
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pillars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                color TEXT NOT NULL
            )
        """)
        await db.execute("""
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
        await db.execute("""
            CREATE TABLE IF NOT EXISTS revenue_streams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                color TEXT NOT NULL
            )
        """)
        
        # Seed pillars if empty
        cursor = await db.execute("SELECT COUNT(*) FROM pillars")
        count = await cursor.fetchone()
        if count[0] == 0:
            pillars_data = [
                ("01", "African-Centered AI Research", "Focus on embedding African languages and indigenous knowledge into AI to create culturally relevant technologies that serve local contexts.", "database", "indigo"),
                ("02", "Educational Transformation", "Use XR and agentic AI technologies to revolutionize education and automate academic workflows for immersive learning.", "monitor", "amber"),
                ("03", "Entrepreneurship Empowerment", "Foster a culture of creators and innovators to promote entrepreneurship within academic communities and beyond.", "users", "emerald"),
                ("04", "Pan-African Innovation Network", "Build collaborative networks between universities and industries across Africa to drive innovation and knowledge sharing.", "share-2", "purple"),
                ("05", "Sustainable Monetization", "Develop diverse revenue streams and marketplaces for AI and XR solutions to ensure long-term sustainability.", "trending-up", "rose"),
                ("06", "Accessibility & Scalability", "Ensure solutions are scalable and accessible across devices using cloud-based architectures and modular platforms.", "cloud", "cyan"),
            ]
            await db.executemany(
                "INSERT INTO pillars (number, title, description, icon, color) VALUES (?, ?, ?, ?, ?)",
                pillars_data,
            )
        
        # Seed architecture layers if empty
        cursor = await db.execute("SELECT COUNT(*) FROM architecture_layers")
        count = await cursor.fetchone()
        if count[0] == 0:
            layers_data = [
                (1, "Experience Layer", "Focuses on immersive and interactive experiences using XR classrooms to provide immersive learning environments with AI-driven interfaces for students and faculty.", "box", "indigo", '["XR Classrooms", "AI Interfaces", "Immersive Learning"]'),
                (2, "Intelligence Layer", "Integrates Generative AI and Agentic AI to provide intelligent decision-making and adaptive learning capabilities through autonomous educational agents.", "cpu", "amber", '["Generative AI", "Agentic Systems", "Adaptive Learning"]'),
                (3, "Data & Integration Layer", "Manages data flow and integrates diverse datasets with secure API Gateway and Event Bus enabling interoperability, scalability, and data sovereignty.", "hard-drive", "emerald", '["Secure APIs", "Data Sovereignty", "System Connectivity"]'),
            ]
            await db.executemany(
                "INSERT INTO architecture_layers (layer_number, title, description, icon, color, tags) VALUES (?, ?, ?, ?, ?, ?)",
                layers_data,
            )
        
        # Seed revenue streams if empty
        cursor = await db.execute("SELECT COUNT(*) FROM revenue_streams")
        count = await cursor.fetchone()
        if count[0] == 0:
            revenue_data = [
                ("XR Modules Marketplace", "Sell XR lessons to schools, corporate partners, and training centers as a core revenue stream, creating a vibrant ecosystem of African-centered educational content.", "package", "purple"),
                ("Corporate & Government Training", "Offer tailored AI and XR courses for professional development in corporate and government sectors, driving digital transformation across industries.", "briefcase", "blue"),
                ("Subscription Access", "Provide premium subscriptions granting students and faculty access to advanced simulations and AI agents, ensuring continuous learning and innovation.", "credit-card", "rose"),
                ("Research Collaboration & Grants", "Engage in joint research projects funded by African and global institutions to drive innovation and establish thought leadership in AI/XR domains.", "award", "cyan"),
            ]
            await db.executemany(
                "INSERT INTO revenue_streams (title, description, icon, color) VALUES (?, ?, ?, ?)",
                revenue_data,
            )
        await db.commit()
