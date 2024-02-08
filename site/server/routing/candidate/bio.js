const express = require("express");
const router = express.Router();
const { getDB } = require("../../mongoClient");


module.exports = router.get("/", async (req, res) => {
    const name = "Candidate Bio Endpoint"
    const { chamber, state, district, firstName, lastName, party } = req.query;
    if (!chamber || !state || !district || !firstName || !lastName || !party) {
        return res.status(400).send("Chamber, state, district, and candidate selections required");
    };
    try {
        const db = getDB();
        const collection = db.collection("2022x");
        const query = {
            election_chamber: chamber,
            election_state: state,
            election_constituency: district,
            candidate_first_name: firstName,
            candidate_last_name: lastName,
            candidate_party: party
        };
        const group = { _id: { firstName, lastName, party } };
        const pipleline = [
            { $match: query },
            { $group: group }
        ];
        const data = await collection.aggregate(pipleline).toArray();
        res.json(data);
        console.log(`${name} | Data: `, data);
    } catch (err) {
        console.error(`${name} | Error:`, err);
        res.status(500).send("Internal server error");
    };
});