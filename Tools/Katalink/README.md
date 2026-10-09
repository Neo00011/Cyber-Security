# ⚔️ Katalink - Advanced Recon & JS Analysis Pipeline

**Katalink** is a powerful Python-based automation tool designed for bug bounty hunters and penetration testers. It bridges the gap between modern crawling engines and deep static analysis by combining **Katana** and **LinkFinder** into a single, streamlined pipeline.

With a single command, Katalink maps out a target's attack surface, strips away noisy static files, eliminates duplicates instantly, and dives into JavaScript files to uncover hidden API endpoints and sensitive secrets.

---

## 🚀 Key Features

* **Automated Web Mapping:** Leverages ProjectDiscovery's **Katana** to crawl modern web applications (including single-page apps)[cite: 3].
* **Intelligent Noise Reduction:** Automatically filters out irrelevant static extensions (`.css`, `.png`, `.jpg`, `.svg`, `.woff`, `.ico`, etc.) to keep your wordlists clean.
* **Instant Duplicate Elimination:** Utilizes memory-optimized Python sets for zero-cost, lightning-fast duplicate removal.
* **Automated JS Analysis:** Automatically isolates discovered JavaScript files and routes them through **LinkFinder** to extract hidden paths and keys.
* **Clean Terminal UI:** Features silent background execution for the crawler and a clean, in-place updating progress counter for the analysis phase.

---

## 🛠️ Tech Stack & Dependencies

Katalink relies on the following tools being installed on your system:
* **Python 3.x**
* **Katana** (ProjectDiscovery) - Must be available in your system `PATH`[cite: 3].
* **LinkFinder** - Ensure `linkfinder.py` is accessible[cite: 3].

---

## ⚙️ Installation

Clone the repository and make sure your dependencies are ready:
