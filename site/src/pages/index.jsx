import React, { useState } from "react";
import Selections from "../components/selections/Selections";
import Candidate from "../components/candidate/Candidate";


export default function Home() {

    const [selectedYear, setSelectedYear] = useState(null);
    const [selectedOffice, setSelectedOffice] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedDistrict, setSelectedDistrict] = useState(null);
    const [selectedCandidate, setSelectedCandidate] = useState(null);

    const handleYearSelection = (year) => {
        setSelectedYear(year);
        setSelectedOffice(null);
    }
    const handleOfficeSelection = (chamber) => {
        setSelectedOffice(chamber);
        setSelectedState(null);
    };
    const handleStateSelection = (state) => {
        setSelectedState(state);
        setSelectedDistrict(null);
    };
    const handleDistrictSelection = (district) => {
        setSelectedDistrict(district);
        setSelectedCandidate(null);
    };
    const handleCandidateSelection = (candidate) => {
        setSelectedCandidate(candidate);
    };

    return (

        <>

        <Selections
            handleYearSelection={handleYearSelection}
            selectedYear={selectedYear}
            handleOfficeSelection={handleOfficeSelection}
            selectedOffice={selectedOffice}
            handleStateSelection={handleStateSelection}
            selectedState={selectedState}
            handleDistrictSelection={handleDistrictSelection}
            selectedDistrict={selectedDistrict}
            handleCandidateSelection={handleCandidateSelection}
        />

        {selectedYear && selectedOffice && selectedState && selectedDistrict && selectedCandidate && (
            <Candidate
                year={selectedYear}
                office={selectedOffice}
                state={selectedState}
                district={selectedDistrict}
                candidate={selectedCandidate}
            />
        )}

        </>

    );

};