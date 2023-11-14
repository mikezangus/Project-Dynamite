import React, { useState, useEffect } from "react";
import "./Dropdown.css";

function formatAmount(amount) {
    return (
        amount >= 10000000 ? `${(amount / 1000000).toFixed(1)}M` : // $60,900,000 => $60.9M
        amount >= 1000000 ? `${(amount / 1000000).toFixed(2)}M` : // $6,090,000 => $6.09M
        amount >= 100000 ? `${(amount / 1000).toFixed(0)}K` : // $609,000 => $609K
        amount >= 10000 ? `${(amount / 1000).toFixed(1)}K` : // $60,900 => $60.9K
        amount >= 1000 ? `${(amount / 1000).toFixed(2)}K` : // $6,090 => $6.09K
        `${amount}` // $609 => $609
    );
};

export default function DropdownCandidates({ selectedDistrict, onSelectedCandidate }) {

    const [candidates, setCandidates] = useState([]);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const fetchCandidates = async () => {
            try {
                if (selectedDistrict) {
                    const [state, district] = selectedDistrict.split("-");
                    const queryParams = new URLSearchParams({ state, district }).toString();
                    const response = await fetch(`http://localhost:4000/api/lastnames?${queryParams}`);
                    if (!response.ok) throw new Error("Network response was not ok");
                    const data = await response.json();
                    setCandidates(data);
                }
            } catch (error) {
                console.error("Error fetching data", error);
            }
        };
        fetchCandidates();
    }, [selectedDistrict]);

    const handleCandidateClick = (candidate) => {
        onSelectedCandidate(candidate);
        setIsOpen(false);
    };

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <main>
            <div className="dropdown">
                <h2 className="dropdown__title">
                    Candidates from {selectedDistrict || ""}
                </h2>
                <button className="dropdown__button" onClick={toggleDropdown}>
                    Click to select a candidate
                </button>
                {isOpen && (
                    <div className="dropdown__menu" style={{ display: "block" }}>
                        {candidates.map((candidateObject) => {
                            const candidateName = candidateObject._id.lastName;
                            const funding = candidateObject.totalFunding;
                            return (
                                <button
                                    className="dropdown__item"
                                    key={candidateName}
                                    onClick={() => handleCandidateClick(candidateObject)}
                                >
                                    {candidateName} - ${formatAmount(funding)}
                                </button>
                            );
                        })}
                    </div>
                )}
            </div>
        </main>
    );
};