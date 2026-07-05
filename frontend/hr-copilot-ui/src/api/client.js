import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000",
});

export async function searchCandidates(jobDescription) {
    const response = await API.post("/jd/search", {
        job_description: jobDescription,
    });

    console.log("[SEARCH API RESPONSE]", response.data);

    return response.data;
}