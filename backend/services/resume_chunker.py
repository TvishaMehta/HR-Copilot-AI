import re

print("\n[CHUNKER LOADED] resume_chunker.py is active\n")


class ResumeChunker:

    HEADER_MAP = {
        "skills": "Skills",
        "technical skills": "Skills",
        "core competencies": "Skills",

        "projects": "Projects",
        "personal projects": "Projects",
        "academic projects": "Projects",

        "experience": "Experience",
        "professional experience": "Experience",
        "work experience": "Experience",
        "employment history": "Experience",

        "education": "Education",
        "certifications": "Certifications",
        "achievements": "Achievements",
        "awards": "Achievements"
    }

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _get_section(self, line: str):
        normalized = line.strip().lower().rstrip(":").replace("&", "and")

        if normalized in self.HEADER_MAP:
            return self.HEADER_MAP[normalized]

        for key in self.HEADER_MAP:
            if key in normalized:
                return self.HEADER_MAP[key]

        return None

    # 🔥 NEW: INLINE HEADER HANDLER
    def _split_inline_header(self, line: str):
        if ":" not in line:
            return None, line

        left, right = line.split(":", 1)
        section = self._get_section(left)

        if section:
            return section, right.strip()

        return None, line

    def chunk_resume(self, resume_text: str):
        resume_text = self._normalize_text(resume_text)

        chunks = []
        current_section = "General"
        current_lines = []
        chunk_id = 1

        lines = resume_text.split("\n")

        for line in lines:

            stripped = line.strip()

            if not stripped:
                continue

            # -----------------------------
            # STEP 1: handle inline headers
            # -----------------------------
            inline_section, content = self._split_inline_header(stripped)

            if inline_section:
                print("[INLINE HEADER]", inline_section, "|", content)

                if current_lines:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                        "metadata": {}
                    })
                    chunk_id += 1
                    print("[CHUNK CREATED]", current_section)

                current_section = inline_section
                current_lines = []

                if content:
                    current_lines.append(content)

                continue

            # -----------------------------
            # STEP 2: normal headers
            # -----------------------------
            section = self._get_section(stripped)

            print("[RAW LINE]", stripped)
            print("[SECTION]", section)

            if section:
                if current_lines:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                        "metadata": {}
                    })
                    chunk_id += 1
                    print("[CHUNK CREATED]", current_section)

                current_section = section
                current_lines = []
                continue

            # -----------------------------
            # STEP 3: normal content
            # -----------------------------
            current_lines.append(stripped)

        # -----------------------------
        # FINAL FLUSH
        # -----------------------------
        if current_lines:
            chunks.append({
                "chunk_id": chunk_id,
                "section": current_section,
                "text": "\n".join(current_lines).strip(),
                "metadata": {}
            })
            print("[FINAL CHUNK CREATED]", current_section)

        print("\n[FINAL CHUNKS COUNT]:", len(chunks))

        return chunks


resume_chunker = ResumeChunker()