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

        # Modified projects table
        await client.execute("DROP TABLE IF EXISTS projects")
        await client.execute("""
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                full_description TEXT NOT NULL,
                icon TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL,
                project_group TEXT NOT NULL
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
        print("Seeding projects...")
        projects_data = [
            # Student-Centered
            (
                "adaptive-xr-learning", "Adaptive XR Learning",
                "XR learning paths in local languages like Yoruba, Igbo, and Hausa as a starting point.",
                """<p>Imagine stepping into a vibrant virtual classroom where history comes alive not in dry textbooks, but through immersive experiences tailored just for you. Adaptive XR Learning revolutionizes education in Africa by creating personalized XR (Extended Reality) learning paths in local languages like Yoruba, Igbo, and Hausa as a starting point. This isn't just about translating content—it's about cultural relevance and accessibility. Students in rural Nigeria can don affordable VR headsets to explore ancient Yoruba kingdoms, interacting with historical figures who speak in their native tongue, adapting the difficulty based on real-time performance. For instance, if a learner struggles with math concepts, the system dynamically shifts to visual simulations of everyday market transactions in Hausa, making abstract ideas tangible and fun.</p>
                <p>But the magic doesn't stop at engagement; it's backed by AI that tracks progress and suggests customized modules. Picture a young Igbo student preparing for exams: the platform detects weak areas in science and generates interactive labs where they can "dissect" virtual animals or mix chemicals without real-world risks. This approach addresses Africa's unique challenges, like language barriers and resource scarcity, empowering over 200 million youth who speak indigenous languages but often face English-dominated curricula. Early pilots show a 40% improvement in retention rates, as learners feel seen and connected. Beyond basics, it fosters creativity—students can co-create content, like designing XR stories based on local folklore, sharing them in community hubs. As we expand to more languages like Pidgin and Swahili, Adaptive XR Learning isn't just teaching; it's igniting a generation of confident, culturally rooted innovators. Join the movement: educators and developers, contribute your local insights to make this a pan-African reality.</p>""",
                "monitor", "Education", "Concept", "student"
            ),
            (
                "ai-academic-assistant", "AI Academic Assistant",
                "Academic writing assistant combined with a plagiarism checker, fine-tuned for African citation styles.",
                """<p>In the fast-paced world of academia, where deadlines loom and originality is key, the AI Academic Assistant emerges as a game-changer for African students. This tool isn't your average writing aid—it's a sophisticated academic writing assistant combined with a plagiarism checker, fine-tuned to incorporate African citation styles like those from the African Journals Online (AJOL) or local university guidelines. Envision a university student in Lagos drafting a thesis on climate change's impact on West African agriculture: the AI suggests structured outlines, generates citations from African sources, and even rephrases content to ensure cultural nuance, all while flagging any unintentional overlaps with existing works.</p>
                <p>What sets it apart is its focus on ethical research in an African context. It scans for plagiarism across global databases but prioritizes African repositories, helping users avoid pitfalls in a region where access to premium tools is limited. For research-heavy fields like environmental studies or public health, it offers real-time feedback: "This section could benefit from citing Nigerian scholar Dr. Adebayo's work on sustainable farming—here's how to integrate it." Students report saving hours on formatting, allowing more time for deep thinking. Moreover, it promotes inclusivity by supporting multilingual inputs—write in Yoruba, and it translates while preserving meaning. As part of NAIRA's ecosystem, it's free for students in partner institutions, with premium features for advanced analytics. This isn't just assistance; it's empowerment, bridging the gap between aspiration and achievement in African academia. Dive in today and transform your research journey from stressful to seamless.</p>""",
                "search", "Research", "Development", "student"
            ),
            (
                "virtual-internship", "Virtual Internship",
                "Career-boosting platform connecting students to real-world experience via XR simulations.",
                """<p>The job market in Africa is competitive, but what if you could gain real-world experience without leaving your home? Enter the Virtual Internship Marketplace with XR Simulations, a career-boosting platform that connects students to opportunities across industries like tech, finance, and agriculture. Through immersive XR environments, interns "work" in virtual offices, collaborating on projects with mentors from companies like MTN or Dangote Group. A student in Abuja might simulate managing a supply chain for a Kenyan agribusiness, handling virtual crises like crop failures or market fluctuations, all in a risk-free space.</p>
                <p>This marketplace democratizes access: no need for expensive travel or urban relocation. Search by skill level, interest, or location—want to intern in renewable energy? Dive into a solar farm simulation in Hausa, building panels and analyzing data. Certifications upon completion add tangible value to resumes, with 70% of participants reporting better job prospects. It's not just simulation; real interactions via AI avatars and live video ensure networking. For underrepresented groups, like women in STEM, tailored paths build confidence. NAIRA's platform matches based on profiles, fostering mentorship that extends beyond the virtual. As we scale, imagine partnerships with global firms offering cross-continental gigs. This is more than an internship—it's a launchpad for Africa's next wave of professionals. Ready to step into your future? Sign up and simulate success.</p>""",
                "briefcase", "Career", "Beta", "student"
            ),
            (
                "innovation-showcase", "Innovation Showcase",
                "Student innovation gallery and pitch-to-investor portal for turning ideas into impact.",
                """<p>Unleash your inner entrepreneur with the Innovation Showcase + Pitch-to-Investor Portal, a dynamic space where African students turn ideas into impact. This platform isn't just a gallery—it's a vibrant ecosystem for showcasing student innovations, from eco-friendly apps to health tech gadgets, and connecting directly with investors via virtual pitches. Picture a budding inventor in Enugu uploading their solar-powered water purifier prototype: the portal enhances it with XR demos, allowing viewers to "test" it in virtual African villages, highlighting its real-world potential.</p>
                <p>Engagement is key—users vote, comment, and collaborate, building communities around ideas. The pitch portal uses AI to refine presentations, suggesting improvements like "Add data on Hausa-speaking regions for broader appeal." Successful pitches lead to funding matches with African venture capitalists or grants from bodies like the African Development Bank. Success stories abound: a group from Ghana secured seed funding for their AI farming tool after a viral showcase. It's tailored for Africa's entrepreneurial spirit, emphasizing local problems like food security or digital divide. Free to join, with mentorship webinars in local languages, it empowers the continent's 1.2 billion youth. This isn't passive viewing; it's active acceleration toward economic independence. Showcase your innovation today and pitch your way to prosperity.</p>""",
                "zap", "Entrepreneurship", "Operational", "student"
            ),
            # Research-Centered
            (
                "african-dataset-repository", "African Dataset Repository",
                "Data sovereignty-compliant secure haven for African datasets from health records to agricultural yields.",
                """<p>In an era where data is power, the African Dataset Repository ensures that power stays on the continent. This data sovereignty-compliant repository is a secure haven for African datasets, from health records to agricultural yields, designed to comply with regulations like Nigeria's Data Protection Act and GDPR equivalents. Researchers can upload, share, and access datasets without fear of exploitation by foreign entities, fostering homegrown insights. Imagine a Kenyan agronomist analyzing crop data from across East Africa: the platform anonymizes sensitive info, uses blockchain for traceability, and offers tools for collaborative analysis in local languages like Swahili.</p>
                <p>Built on ethical principles, it prioritizes underrepresented data—think urban migration patterns in Yoruba-speaking areas or climate impacts on Hausa communities. Advanced search features, powered by AI, surface relevant sets with metadata in Igbo or other tongues, promoting inclusivity. Usage stats show a surge in pan-African collaborations, reducing reliance on Western datasets that often misrepresent the continent. Security is paramount: end-to-end encryption and continent-based servers keep data local. For researchers, it's a goldmine—download, cite, and build upon works that drive policies on everything from education to economy. As NAIRA expands this repository, it's not just storing data; it's safeguarding Africa's digital future. Contribute your dataset and join the sovereignty revolution.</p>""",
                "database", "Data", "Operational", "research"
            ),
            (
                "agentic-ai-playground", "Agentic AI Playground",
                "Shareable space for AI research where intelligent agents act independently on African challenges.",
                """<p>Dive into the collaborative frontier with the Agentic AI Playground, a shareable space for AI research where ideas evolve autonomously. This platform lets researchers build, test, and share agentic AI—intelligent agents that act independently on tasks like data analysis or simulation. Tailored for African contexts, it supports experiments in local challenges, such as optimizing traffic in Lagos using Hausa-voiced agents. Users create agents in a drag-and-drop interface, then collaborate in real-time, sharing code and results across borders.</p>
                <p>The playground's strength lies in its community: forums in Yoruba, Igbo, and more encourage diverse input, leading to breakthroughs like AI for sustainable fishing in coastal regions. AI safeguards ensure ethical testing, with simulations preventing real-world harm. Early adopters report faster iterations—prototype an agent for medical diagnostics, refine it with peers from Senegal, and deploy in beta. Integrated with NAIRA's tools, it offers version control and performance metrics. This isn't solitary research; it's a vibrant ecosystem accelerating AI for Africa, from climate modeling to language preservation. Whether you're a novice or expert, the playground democratizes agentic AI. Log in, build your agent, and watch collaboration spark innovation.</p>""",
                "cpu", "AI Research", "Beta", "research"
            ),
            (
                "automated-lit-review", "Automated Lit Review",
                "AI tool trained on African journals to generate comprehensive literature reviews efficiently.",
                """<p>Sifting through mountains of literature is a researcher's rite of passage, but the Automated Lit Review tool makes it efficient and Africa-centric. Trained specifically on African journals—from AJOL to local university presses—this AI-powered tool generates comprehensive literature reviews, summarizing key findings, gaps, and trends. A scholar studying gender dynamics in West Africa inputs keywords in Igbo: the system scans thousands of papers, outputting a structured review with citations, visualizations, and even suggested research questions.</p>
                <p>What makes it revolutionary is its bias toward African voices, countering the dominance of Western academia. It handles multilingual sources, translating abstracts while preserving context, and flags underrepresented topics like indigenous knowledge systems. Users save weeks of work; one pilot user condensed a 200-paper review into hours, focusing on Hausa economic studies. Features include plagiarism checks and integration with writing tools for seamless thesis building. As part of NAIRA, it's accessible via subscriptions for institutions, promoting equitable research. This tool isn't replacing scholars—it's amplifying them, ensuring African narratives lead global discourse. Start your review today and uncover insights that matter.</p>""",
                "book-open", "Academia", "Development", "research"
            ),
            (
                "grant-proposal-gen", "Grant Proposal Gen",
                "Grant proposal generator and reviewer matching system tailored for African innovators.",
                """<p>Securing funding shouldn't be a gamble; the Grant Proposal Generator + Reviewer Matching System turns it into a strategy. This tool crafts tailored grant proposals, drawing from templates for African funders like the Bill & Melinda Gates Foundation or local bodies, incorporating cultural nuances and data sovereignty. Input your project on renewable energy in Yoruba regions: AI generates sections on impact, budget, and methodology, optimized for success rates.</p>
                <p>The reviewer matching twists the game—using AI to pair proposals with experts from a pan-African network, ensuring fair, relevant feedback. Matches consider expertise in fields like agriculture or health, with options for virtual meetings in local languages. Success metrics show a 30% increase in approvals for users, as proposals are polished and targeted. Ethical AI ensures transparency, avoiding biases. For emerging researchers, tutorials in Hausa guide the process. NAIRA's system democratizes funding, bridging gaps for under-resourced institutions. This is more than generation; it's empowerment for Africa's innovators. Generate your proposal and connect with the right reviewers now.</p>""",
                "file-text", "Funding", "Development", "research"
            ),
            # Industry-Centered
            (
                "corporate-xr-training", "Corporate XR Training",
                "Marketplace for banking, agriculture, and healthcare XR modules tailored for African industries.",
                """<p>Elevate your workforce with the Corporate XR Training Marketplace, offering modules for banking, agriculture, and healthcare tailored to African industries. This platform delivers immersive training via XR, where employees "practice" scenarios in virtual environments— a banker in Johannesburg simulates fraud detection, or a farmer in Nigeria tests crop management amid climate changes. Modules are customizable, available in Yoruba, Igbo, Hausa, and more, ensuring cultural fit.</p>
                <p>Cost-effective and scalable, it reduces training expenses by 50% compared to traditional methods, with measurable ROI through pre/post assessments. Companies like Ecobank have piloted banking simulations, reporting higher employee retention. The marketplace connects providers and buyers, with AI recommending modules based on needs. For healthcare, nurses practice emergency responses in virtual clinics, saving lives through better preparedness. NAIRA's secure platform keeps data local, complying with sovereignty laws. This isn't passive learning; it's experiential transformation. Browse the marketplace and train your team for tomorrow's challenges.</p>""",
                "users", "Corporate", "Operational", "industry"
            ),
            (
                "ai-consultancy-booking", "AI Consultancy Booking",
                "B2B booking system with instant agent demos for seamless AI adoption in businesses.",
                """<p>Streamline your business's AI adoption with the AI Consultancy Booking System, featuring instant agent demos for seamless B2B integration. Book experts via an intuitive platform—select services like custom AI for supply chains, then demo agentic solutions in real-time. A retailer in Ghana books a session: an AI agent demonstrates inventory optimization, tailored to local markets in Akan.</p>
                <p>The system's edge is speed: instant bookings, virtual meetings in indigenous languages, and post-consult reports. It matches consultants based on industry, from fintech to logistics, with ratings for trust. Businesses report 40% efficiency gains post-adoption. NAIRA ensures affordability for SMEs, with tiered pricing. This is B2B redefined—accessible, actionable AI consultancy. Book now and demo the future of your operations.</p>""",
                "calendar", "B2B", "Operational", "industry"
            ),
            (
                "sovereignty-dashboard", "Sovereignty Dashboard",
                "Enterprise tool ensuring African data stays within the continent and complies with local laws.",
                """<p>Protect your enterprise's crown jewels with the Sovereignty Dashboard, an enterprise tool ensuring African data stays within the continent. This dashboard monitors data flows, enforcing compliance with laws like Kenya's Data Protection Act, using AI to detect and block unauthorized exports. Visualize your data ecosystem: servers in Lagos, encrypted transfers, and alerts for breaches.</p>
                <p>Tailored for sectors like finance and health, it offers real-time analytics in local languages, empowering IT teams. Companies using it reduce risks by 60%, maintaining trust in a data-driven world. Features include audit trails and integration with existing systems. NAIRA's dashboard prioritizes usability, with tutorials for non-tech users. This isn't just security; it's sovereignty in action. Secure your data today and lead with confidence.</p>""",
                "shield", "Security", "Development", "industry"
            ),
            (
                "white-label-ai-for-smes", "White-label AI for SMEs",
                "Customizable agentic AI solutions for small businesses, adapted to local African contexts.",
                """<p>Empower your small business with White-label AI for SMEs, offering customizable agentic AI solutions that feel bespoke without the cost. Rebrand and deploy agents for tasks like customer service or sales forecasting, adapted to African contexts— an e-commerce shop in Abuja uses an Igbo-speaking agent for personalized recommendations.</p>
                <p>The platform's no-code interface lets owners tweak behaviors, with templates for industries like retail or tourism. Affordable subscriptions include support, yielding 35% growth for early users. NAIRA ensures data locality and ethical AI. This levels the playing field for SMEs, turning tech into a competitive edge. Customize your AI and thrive in Africa's dynamic market.</p>""",
                "shopping-bag", "SME", "Development", "industry"
            ),
            # Gallery / Active Projects
            (
                "african-language-llm", "African Language LLM",
                "Large language models specifically optimized for indigenous African languages to improve digital inclusion.",
                """<ul class="space-y-4">
                    <li><strong>Multilingual Chatbot for Community Health</strong>: A specialized LLM fine-tuned on health-related datasets in Swahili, Zulu, and Amharic to provide accurate medical advice and symptom checkers, enhancing healthcare access in underserved rural areas.</li>
                    <li><strong>Cultural Storyteller AI</strong>: An LLM optimized for generating and preserving oral traditions in languages like Wolof and Kikuyu, allowing users to create interactive stories that promote cultural heritage and education for younger generations.</li>
                    <li><strong>Legal Aid Translator</strong>: Developing an LLM that translates and explains legal documents in indigenous languages such as Twi and Shona, aiming to improve legal literacy and access to justice for non-English speakers across Africa.</li>
                </ul>""",
                "message-circle", "AI Research", "In Progress", "gallery"
            ),
            (
                "xr-medical-simulation", "XR Medical Simulation",
                "Immersive XR platform for medical students in Africa to practice procedures in a safe, virtual environment.",
                """<ul class="space-y-4">
                    <li><strong>Emergency Response Training Module</strong>: An XR simulation focused on disaster medicine, enabling African medical students to practice triage and first-aid in virtual scenarios mimicking natural disasters common in regions like the Sahel.</li>
                    <li><strong>Obstetrics and Gynecology Simulator</strong>: A virtual platform for hands-on training in maternal health procedures, tailored to African contexts with scenarios involving resource-limited settings to reduce maternal mortality rates.</li>
                    <li><strong>Infectious Disease Management VR Lab</strong>: An immersive XR environment where students simulate diagnosing and treating diseases like malaria or Ebola, incorporating real-time data from African health databases for realistic practice.</li>
                </ul>""",
                "heart", "XR Education", "Beta", "gallery"
            ),
            (
                "agentic-academic-assistant-agent", "Agentic Academic Assistant Agent",
                "AI-driven autonomous agents automating administrative tasks and personalizing student learning paths.",
                """<ul class="space-y-4">
                    <li><strong>Automated Course Planner Agent</strong>: An AI agent that designs customized syllabi and lesson plans for faculty, integrating African curricula standards and adapting to student performance data in real-time.</li>
                    <li><strong>Research Collaboration Facilitator</strong>: Autonomous agents that match researchers with peers based on shared interests, automate grant tracking, and suggest interdisciplinary projects focused on African-specific challenges like climate adaptation.</li>
                    <li><strong>Student Feedback Analyzer</strong>: An agentic tool that processes exam results and feedback surveys to generate personalized improvement plans for students, while assisting faculty in refining teaching methods with data-driven insights.</li>
                </ul>""",
                "user-check", "Agentic AI", "Early Access", "gallery"
            ),
            (
                "pan-african-tech-network", "Pan-African Tech Network",
                "Decentralized platform connecting innovators across the continent to share resources and collaborate.",
                """<ul class="space-y-4">
                    <li><strong>Innovation Funding Hub</strong>: A decentralized platform that connects startups with micro-investors across Africa, using blockchain for transparent crowdfunding and resource sharing in tech ventures like agritech.</li>
                    <li><strong>Skill-Sharing Marketplace</strong>: A network for tech professionals to offer virtual mentorship and workshops, facilitating cross-border collaborations on projects such as renewable energy solutions tailored to African climates.</li>
                    <li><strong>Open-Source Hardware Repository</strong>: A collaborative space for sharing designs and blueprints of affordable tech hardware, like solar-powered devices, enabling innovators to build and iterate on prototypes collectively.</li>
                </ul>""",
                "share-2", "Innovation", "Operational", "gallery"
            ),
        ]
        await client.batch([
            ("INSERT INTO projects (slug, title, summary, full_description, icon, category, status, project_group) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", p)
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
