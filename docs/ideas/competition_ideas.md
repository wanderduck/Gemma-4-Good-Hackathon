# Gemma 4 Good Hackathon - Competition Ideas

Ideas organized by competition track, designed to leverage Gemma 4's strengths: local inference, multimodal understanding, native function calling, and open weights.

---

## B) Global Resilience

### 1. Offline Disaster Damage Triage
A mobile-first tool for first responders in connectivity-dead-zones after earthquakes, hurricanes, or floods. Take a photo of a building, and Gemma 4 (fine-tuned on structural damage datasets) classifies severity, estimates habitability, and generates a standardized damage report — all running locally. Function calling drives a priority queue that helps coordinate rescue teams without a server.

### 2. Community Climate Adaptation Planner
An agentic system that ingests local climate projection data (NOAA, IPCC downscaled models) and helps small municipalities plan for floods, heat, or drought. Users describe their community ("farming town, 5000 people, river runs through downtown") and the agent retrieves relevant projections, identifies vulnerabilities, and generates an actionable adaptation plan with cost estimates. Targets the gap where small towns can't afford climate consultants.

### 3. Multilingual Early Warning Translator
Disaster warnings fail when they're in the wrong language or too technical. This tool takes official government emergency alerts and instantly translates them into locally-spoken languages and reading levels — including generating audio for low-literacy populations. Fine-tuned on emergency communication guidelines (FEMA, WHO) to preserve urgency and actionable detail rather than producing generic translations.

### 4. Crop Failure & Food Security Monitor
A local-first tool for agricultural extension workers in developing regions. Upload photos of crops showing disease, pest damage, or drought stress; Gemma 4 identifies the issue, recommends interventions using local resource constraints, and tracks regional patterns over time. Runs offline on a laptop in the field, syncs when connectivity returns.

---

## C) Future of Education

### 1. Socratic Lab Partner
An AI lab partner for science students that never gives answers — only asks questions. Students describe their experiment, observations, or confusion, and the agent guides them through reasoning using Socratic method. It tracks the student's conceptual model over a session and targets specific misconceptions. Designed for underfunded schools where lab time is limited and teacher-to-student ratios are high.

### 2. Teacher Prep Copilot
An agent that helps teachers create differentiated lesson materials in minutes. Describe a topic and your class profile (grade level, reading levels, IEP accommodations, language backgrounds), and it generates multiple versions of the same lesson — simplified, advanced, visual-heavy, ESL-adapted — plus formative assessment questions aligned to standards. Function calling integrates with curriculum databases.

### 3. Thesis Defense Simulator
A tool for graduate students (or advanced undergrads) preparing to defend research. Upload a paper or thesis draft, and Gemma 4 role-plays as a panel of examiners — asking tough questions, probing methodology, challenging conclusions. It adapts difficulty based on the student's responses and provides feedback on argumentation quality. Nothing like this exists and it demos spectacularly.

### 4. Hands-On Trade Skills Tutor
Targets vocational/trade education (electricians, plumbers, welders). Students photograph their work-in-progress (a wiring job, a pipe fitting, a weld bead), and Gemma 4 evaluates quality, identifies code violations or safety issues, and explains corrections — with reference to actual trade codes. Addresses the massive skilled-trades shortage and the fact that these students are underserved by current AI tools.

---

## D) Digital Equity & Inclusivity

### 1. Language Revitalization Engine
A tool for indigenous and endangered language communities. Community members contribute word lists, phrases, and audio; the system (fine-tuned with whatever data exists) becomes a learning tool, dictionary, and translation aid for the community's language. Runs locally so data sovereignty stays with the community. Even partial capability for a language with zero existing AI support is groundbreaking.

### 2. Plain Language Government Navigator
Government services (benefits, permits, legal rights) are buried in jargon and labyrinthine websites. This agent takes a person's situation in plain language ("I lost my job and have two kids") and tells them exactly what they qualify for, how to apply, and what documents they need — in their language, at their reading level. Function calling retrieves current eligibility rules from public APIs.

### 3. AI Literacy Coach for Non-Technical Users
An interactive coach that teaches everyday people how to use AI tools effectively and safely — not by lecturing, but by guided practice. It walks users through real tasks (writing a resume, understanding a medical report, comparing products), teaches them prompting by doing, and builds their intuition for when AI is reliable vs. when to be skeptical. Closes the AI skills gap directly.

### 4. Accessible Document Transformer
Upload any document (PDF, image, scanned form) and this tool makes it accessible: generates alt-text for images, converts complex tables to screen-reader-friendly formats, simplifies dense legal/medical language, and produces audio summaries. Targets the 1B+ people with disabilities who face daily barriers to information access. Multimodal Gemma 4 is uniquely suited here.

### 5. Offline Digital Literacy Hub
A self-contained, offline-capable learning environment for communities with limited or no internet. Pre-loaded with locally-relevant content (health info, agricultural guides, civic education), it runs on cheap hardware and lets users ask questions in natural language. Designed for rural libraries, community centers, and NGO field offices. The edge deployment story writes itself for the demo.

---

## E) Safety & Trust

### 1. Source Verification Agent
A tool that takes any claim or article and systematically checks it: extracts key claims, searches for corroborating/contradicting sources via function calling, evaluates source credibility, and presents a structured "trust report" with confidence levels and reasoning chains. The user sees exactly why something is rated trustworthy or suspect — full transparency.

### 2. AI Decision Explainer
When AI systems make consequential decisions (loan approvals, hiring screens, medical risk scores), affected people deserve explanations. This tool takes an AI model's output and the input data, then generates human-readable explanations of what factors drove the decision, what would change the outcome, and what recourse exists. Targets the "right to explanation" gap.

### 3. Local-First Privacy Vault
A completely offline AI assistant for sensitive domains — legal consultations, medical questions, financial planning, domestic violence resources. The key insight: many people who need AI help most won't use cloud services because the data is too sensitive. Gemma 4 running locally means nothing leaves the device. The demo shows sensitive queries that users would never type into ChatGPT.

### 4. Misinformation Inoculation Trainer
Rather than fact-checking after the fact, this tool trains users to recognize manipulation techniques proactively. It generates realistic examples of common misinformation patterns (emotional manipulation, cherry-picked statistics, fake authority), has the user try to spot the tricks, then explains the techniques. Based on the "prebunking" research from Cambridge/Google. Interactive and demo-friendly.
