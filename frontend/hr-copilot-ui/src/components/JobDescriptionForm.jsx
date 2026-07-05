import { useState } from "react";

export default function JobDescriptionForm({ onSearch }) {
    const [jobDescription, setJobDescription] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        alert("Button clicked!");

        console.log(jobDescription);

        onSearch(jobDescription);
    };

    return (
        <form onSubmit={handleSubmit}>
            <textarea
                rows={8}
                cols={80}
                placeholder="Paste Job Description..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
            />

            <br />
            <br />

            <button type="submit">
                Search Candidates
            </button>
        </form>
    );
}