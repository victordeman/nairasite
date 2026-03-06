import asyncio
import os
import libsql_client

# Use Turso Database URL and Auth Token from environment variables
if os.getenv("TURSO_DATABASE_URL"):
    DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
elif os.getenv("VERCEL"):
    DATABASE_URL = "file:/tmp/naira.db"
else:
    DATABASE_URL = "file:naira.db"

AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

async def migrate():
    print(f"Connecting to {DATABASE_URL}...")
    async with libsql_client.create_client(url=DATABASE_URL, auth_token=AUTH_TOKEN) as client:
        print("Creating tables...")
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
                summary TEXT NOT NULL DEFAULT '',
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
        await client.execute("""
            CREATE TABLE IF NOT EXISTS vision_missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                color TEXT NOT NULL
            )
        """)

        print("Checking if seeding is needed...")
        
        # Seed pillars
        cursor = await client.execute("SELECT COUNT(*) FROM pillars")
        if cursor.rows[0][0] == 0:
            print("Seeding pillars...")
            pillars_data = [
                ("01", "African-Centered AI Research", "In the realm of African-Centered AI Research, NAIRA is pioneering a paradigm shift by infusing artificial intelligence with the rich tapestry of Africa's indigenous knowledge systems. This pillar emphasizes the integration of local languages, cultural narratives, and traditional wisdom into AI models.", "In the realm of African-Centered AI Research, NAIRA is pioneering a paradigm shift by infusing artificial intelligence with the rich tapestry of Africa's indigenous knowledge systems. This pillar emphasizes the integration of local languages, cultural narratives, and traditional wisdom into AI models, ensuring that technologies are not just functional but deeply resonant with African contexts. A special focus here is on Igbo heritage, one of Nigeria's most vibrant cultural legacies, which embodies communal resilience, intricate storytelling, and profound philosophical insights. For instance, Igbo proverbs—such as \"Onye kwe, chi ya ekwe\" (If a person agrees, their spirit agrees)—offer timeless lessons in consensus-building and personal agency that can inform ethical AI decision-making algorithms. By training large language models (LLMs) on Igbo folklore, oral histories, and artistic expressions like the intricate Uli body art patterns, we create AI systems that recognize and generate content in Igbo dialects, preserving endangered linguistic nuances while enabling applications in healthcare, agriculture, and governance. Imagine AI-powered chatbots that dispense farming advice drawing from Igbo agrarian traditions, or virtual reality simulations that recreate masquerade festivals to educate global audiences. This approach not only combats cultural erosion but also positions Africa as a leader in ethical AI, transforming the technological landscape by ensuring inclusivity and relevance. Through collaborations with Igbo scholars and communities, NAIRA is building datasets that celebrate this heritage, fostering AI that empowers rather than erases identities, and sparking a wave of innovation that honors the continent's diverse roots.", "database", "indigo"),
                ("02", "Educational Transformation", "Educational Transformation stands as a cornerstone of NAIRA's strategy, leveraging XR and agentic AI to revolutionize learning across Africa. In a continent where access to quality education remains uneven, this pillar deploys immersive technologies to create virtual classrooms that transcend physical limitations.", "Educational Transformation stands as a cornerstone of NAIRA's strategy, leveraging XR and agentic AI to revolutionize learning across Africa. In a continent where access to quality education remains uneven, this pillar deploys immersive technologies to create virtual classrooms that transcend physical limitations, automating workflows and personalizing experiences for students and educators alike. Picture medical students in rural Nigeria practicing complex surgeries through haptic-feedback XR simulations, or history lessons where learners step into ancient African kingdoms via augmented reality. Agentic AI agents act as intelligent tutors, adapting curricula in real-time based on individual progress, while automating administrative tasks like grading and scheduling to free teachers for creative mentoring. This not only bridges the digital divide but also embeds African perspectives into global knowledge, such as integrating Swahili literature or Zulu mathematics into adaptive learning paths. By 2030, we envision a transformed landscape where dropout rates plummet, skills gaps close, and a new generation of African innovators emerges, equipped to tackle climate change, urbanization, and economic challenges. Through scalable pilots in partner universities, NAIRA is proving that technology can democratize education, turning Africa's youthful population into a powerhouse of informed, agile thinkers ready to lead the world's next technological wave.", "monitor", "amber"),
                ("03", "Entrepreneurship Empowerment", "Entrepreneurship Empowerment ignites the spark of innovation within Africa's academic and community ecosystems, cultivating a culture of creators who turn ideas into impactful ventures. This pillar addresses the continent's high youth unemployment by providing tools, mentorship, and AI-driven resources.", "Entrepreneurship Empowerment ignites the spark of innovation within Africa's academic and community ecosystems, cultivating a culture of creators who turn ideas into impactful ventures. This pillar addresses the continent's high youth unemployment by providing tools, mentorship, and AI-driven resources to nurture startups from conception to scale. Using agentic AI, aspiring entrepreneurs can simulate business models, predict market trends informed by local data, and access virtual incubators that connect them with investors. For example, an XR platform might allow a young inventor in Lagos to prototype sustainable energy solutions in a collaborative virtual space, drawing on real-time feedback from peers across borders. We emphasize skill-building in AI ethics, digital marketing, and sustainable practices, ensuring ventures align with Africa's needs—like affordable tech for smallholder farmers or eco-friendly urban planning. By fostering this entrepreneurial spirit, NAIRA transforms the technological landscape, shifting from aid dependency to self-reliant innovation hubs. Success stories from our programs highlight how empowered youth are launching AI apps for language translation or XR training for artisans, creating jobs and economic ripple effects that uplift entire communities and position Africa as a global exporter of tech solutions.", "users", "emerald"),
                ("04", "Pan-African Innovation Network", "The Pan-African Innovation Network weaves a tapestry of collaboration, linking universities, industries, and governments across the continent to accelerate knowledge exchange and joint problem-solving. This pillar combats fragmentation by creating digital platforms for co-developing AI tools.", "The Pan-African Innovation Network weaves a tapestry of collaboration, linking universities, industries, and governments across the continent to accelerate knowledge exchange and joint problem-solving. This pillar combats fragmentation by creating digital platforms where researchers from Senegal to South Africa can co-develop AI tools tailored to shared challenges like food security and public health. Through virtual conferences, shared XR labs, and AI-facilitated matchmaking, we build bridges that amplify collective intelligence. Imagine Ethiopian engineers partnering with Kenyan coders to design drought-resistant crop prediction models, or Moroccan startups collaborating with Nigerian firms on renewable energy AI. By prioritizing open-source initiatives and cross-border funding, NAIRA ensures equitable participation, transforming Africa's tech landscape from isolated pockets of excellence to a unified force. This network not only speeds up innovation cycles but also influences global standards, showcasing African solutions at international forums and attracting investments that fuel sustainable growth.", "share-2", "purple"),
                ("05", "Sustainable Monetization", "Sustainable Monetization ensures NAIRA's longevity by diversifying revenue streams that support ongoing AI and XR development without compromising our mission. This pillar creates marketplaces for XR educational modules, generating funds reinvested into research.", "Sustainable Monetization ensures NAIRA's longevity by diversifying revenue streams that support ongoing AI and XR development without compromising our mission. This pillar creates marketplaces for XR educational modules, where schools and corporations purchase culturally attuned content, generating funds reinvested into research. Premium subscriptions offer advanced AI agents for personalized learning, while corporate training programs deliver tailored XR courses on digital transformation. Grants from global institutions fund collaborative projects, and affiliate models reward content creators. By embedding monetization into our ecosystem—like selling Igbo-language AI datasets—we build financial resilience, transforming Africa's tech landscape into a self-sustaining powerhouse. This approach avoids over-reliance on donors, instead creating value chains that empower local economies and ensure innovations reach those who need them most.", "trending-up", "rose"),
                ("06", "Accessibility & Scalability", "Accessibility & Scalability guarantees that NAIRA's solutions reach every corner of Africa, using cloud-based architectures and modular designs to adapt across devices. This pillar prioritizes low-bandwidth optimizations and offline capabilities.", "Accessibility & Scalability guarantees that NAIRA's solutions reach every corner of Africa, using cloud-based architectures and modular designs to adapt across devices—from high-end VR headsets to basic smartphones. This pillar prioritizes low-bandwidth optimizations and offline capabilities, ensuring rural users in remote villages can access AI-driven education without reliable internet. By employing scalable microservices and edge computing, we handle growing user bases seamlessly, while open standards promote interoperability. For instance, an XR app teaching sustainable farming could run on affordable Android devices, incorporating voice commands in local languages. This democratizes technology, transforming the continent's landscape by closing accessibility gaps and enabling massive adoption, ultimately fostering inclusive growth where no one is left behind in the AI revolution.", "cloud", "cyan"),
            ]
            await client.batch([
                ("INSERT INTO pillars (number, title, summary, description, icon, color) VALUES (?, ?, ?, ?, ?, ?)", p)
                for p in pillars_data
            ])

        # Seed architecture layers
        cursor = await client.execute("SELECT COUNT(*) FROM architecture_layers")
        if cursor.rows[0][0] == 0:
            print("Seeding architecture layers...")
            layers_data = [
                (1, "Experience Layer", "Focuses on immersive and interactive experiences using XR classrooms to provide immersive learning environments with AI-driven interfaces for students and faculty.", "box", "indigo", '["XR Classrooms", "AI Interfaces", "Immersive Learning"]'),
                (2, "Intelligence Layer", "Integrates Generative AI and Agentic AI to provide intelligent decision-making and adaptive learning capabilities through autonomous educational agents.", "cpu", "amber", '["Generative AI", "Agentic Systems", "Adaptive Learning"]'),
                (3, "Data & Integration Layer", "Manages data flow and integrates diverse datasets with secure API Gateway and Event Bus enabling interoperability, scalability, and data sovereignty.", "hard-drive", "emerald", '["Secure APIs", "Data Sovereignty", "System Connectivity"]'),
            ]
            await client.batch([
                ("INSERT INTO architecture_layers (layer_number, title, description, icon, color, tags) VALUES (?, ?, ?, ?, ?, ?)", l)
                for l in layers_data
            ])

        # Seed revenue streams
        cursor = await client.execute("SELECT COUNT(*) FROM revenue_streams")
        if cursor.rows[0][0] == 0:
            print("Seeding revenue streams...")
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

        # Seed projects
        cursor = await client.execute("SELECT COUNT(*) FROM projects")
        if cursor.rows[0][0] == 0:
            print("Seeding projects...")
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

        # Seed vision missions
        cursor = await client.execute("SELECT COUNT(*) FROM vision_missions")
        if cursor.rows[0][0] == 0:
            print("Seeding vision missions...")
            vision_data = [
                (
                    "ai-excellence-hub",
                    "AI Excellence Hub",
                    "Positioning NBU as a premier AI center in Nigeria and across Africa, setting global standards for African-centered technological innovation.",
                    """<p>The AI Excellence Hub represents NAIRA’s bold ambition to establish Nnamdi Azikiwe University (NBU) as the undisputed flagship institution for artificial intelligence on the African continent. This is not merely about building another research lab or training more data scientists — it is about creating a world-class epicenter where African priorities, values, languages, philosophies, and lived realities become the foundational inputs for next-generation AI systems.</p>
                    <p>Rather than continuing the historical pattern of adopting foreign AI models and retrofitting them with limited African data, NAIRA is inverting the paradigm. We are designing, training, and deploying AI architectures that are African-first from the ground up. This means large language models whose pre-training corpora give equal — or even preferential — weight to Hausa oral epics, Yoruba Ifá divination verses, Igbo proverbs and masquerade ontologies, Akan drum language patterns, Amharic Ge’ez script traditions, Kiswahili coastal poetry, Shona mbira tunings, and San click-language storytelling, among hundreds of other knowledge systems.</p>
                    <p>At the heart of the Excellence Hub lies a commitment to cultural fidelity in model behavior. When an NAIRA-trained model is asked ethical questions, it draws reasoning patterns not only from Western philosophy but also from Ubuntu (“I am because we are”), from the Akan concept of Sankofa (“go back and get it”), from Igbo chi personal-spirit agency, and from Yoruba ori destiny-responsibility frameworks. When it generates educational content, it naturally embeds local metaphors, seasonal agricultural cycles, kinship structures, and indigenous taxonomies rather than defaulting to Euro-American defaults.</p>
                    <p>The physical and digital infrastructure of the Hub is deliberately Pan-African in character. We maintain high-performance GPU clusters co-located in Awka with mirrored edge nodes in Addis Ababa, Nairobi, Dakar, Cape Town, and Kigali — creating sub-50 ms inference latency across most population centers. Open datasets released under permissive African-centered licenses (inspired by but distinct from Creative Commons) are already being used by universities in Ghana, Kenya, Rwanda, Senegal, and South Africa.</p>
                    <p>NAIRA’s researchers are publishing in top-tier venues while simultaneously producing high-impact local-language technical reports, video explainers in Pidgin, Igbo, Yoruba, Hausa, and Amharic, and XR-based interactive tutorials that allow secondary-school students in rural communities to understand transformer attention mechanisms through visual storytelling rooted in their own cultural idioms.</p>
                    <p>By 2030, the goal is unambiguous: when global institutions, development agencies, philanthropies, or tech companies want to understand responsible, inclusive, culturally-grounded AI for the majority world, the first institution they reference — and visit — will be NAIRA at NBU. We are not trying to catch up to Silicon Valley or Shenzhen. We are building a distinct African pole of AI excellence that the rest of the world will eventually need to learn from.</p>""",
                    "target",
                    "indigo"
                ),
                (
                    "regional-leadership",
                    "Regional Leadership",
                    "Leading Africa's AI-driven innovation and global competitiveness through cutting-edge research and applications.",
                    """<p>Regional Leadership means NAIRA does not view itself as an isolated academic institute pursuing publications and grants. Instead, we see ourselves as the strategic orchestrator and accelerator of an Africa-wide AI innovation ecosystem that must collectively move the continent from technology consumer → technology co-producer → technology agenda-setter on the global stage.</p>
                    <p>This leadership manifests in several interlocking dimensions:</p>
                    <ul class="list-disc pl-6 space-y-4 mt-4">
                        <li><strong>Benchmark-defining research programs</strong>: We are deliberately targeting grand challenges where Africa has both the greatest need and — paradoxically — structural advantages: multilingual low-resource language modeling, climate-adaptive agriculture AI, decentralized health diagnostics in low-connectivity environments, ethical autonomous financial inclusion systems, and culturally-safe child-protective content moderation.</li>
                        <li><strong>Pan-African capability diffusion</strong>: Through the NAIRA Fellows program, annual Summer AI Intensives hosted rotationally across ECOWAS, EAC, SADC, and North African university partners, train-the-trainer bootcamps for polytechnics, and open XR-based “AI Literacy Caravans” that travel to secondary schools, we are rapidly widening the base of African AI practitioners.</li>
                        <li><strong>Industry co-creation pipelines</strong>: We maintain formal innovation partnerships with African fintech unicorns, agritech scale-ups, healthtech consortia, edtech platforms, and renewable energy companies. These are not consulting arrangements — they are joint R&D labs where NAIRA researchers and company engineers co-own IP under clearly defined African-benefit clauses.</li>
                        <li><strong>Global agenda-setting presence</strong>: NAIRA leads or co-leads African delegations to major AI governance forums (UN Global Digital Compact, GPAI, UNESCO AI Ethics negotiations, AfCFTA digital trade working groups).</li>
                        <li><strong>Competitive positioning in the global value chain</strong>: By building sovereign model stacks, open-weight culturally-aligned foundation models, high-quality African-language evaluation suites, and verifiable data-provenance infrastructure, NAIRA is helping position African nations to capture higher-value segments of the global AI supply chain.</li>
                    </ul>
                    <p class="mt-6">In short, Regional Leadership is the conviction that Africa’s AI future will not be gifted by external powers, nor will it emerge spontaneously from market forces alone. It must be deliberately constructed through coordinated, high-ambition research, aggressive talent multiplication, strategic industry alignment, and unapologetic global advocacy. NAIRA exists to be the institution that makes that coordinated ascent both technically feasible and politically credible.</p>""",
                    "globe",
                    "amber"
                )
            ]
            await client.batch([
                ("INSERT INTO vision_missions (slug, title, summary, description, icon, color) VALUES (?, ?, ?, ?, ?, ?)", v)
                for v in vision_data
            ])

    print("Migration and seeding complete.")

if __name__ == "__main__":
    asyncio.run(migrate())
