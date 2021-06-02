
const getStates = async () => {
    let stateList = JSON.parse(localStorage.getItem("states"));
    if (stateList == null) {
        let states = await fetch('/needs/getState');
        states = await states.json();
        let stateList = [];
        states.forEach(element => {
            stateList.push(element);
            let tag = `<option value="${String(element)}" style="text-transform: capitalize;">`;
            $("#states").append(tag);
        });

        localStorage.setItem("states", JSON.stringify(stateList));
    }
    else {
        console.log("Fetching from local storage");
        stateList.forEach(element => {
            let tag = `<option value="${String(element)}" style="text-transform: capitalize;">`;
            $("#states").append(tag);
        });
    }

}
const getDistrict = async () => {
    let districtList = JSON.parse(localStorage.getItem("districts"));
    if (districtList == null) {
        let districts = await fetch('/needs/getDistrict');
        districts = await districts.json();
        let districtList = [];
        districts.forEach(element => {
            districtList.push(element);
            let tag = `<option value="${String(element)}" style="text-transform: capitalize;">`;
            $("#district").append(tag);
        });

        localStorage.setItem("districts", JSON.stringify(districtList));
    }
    else {
        console.log("Fetching from local storage");
        stateList.forEach(element => {
            let tag = `<option value="${String(element)}" style="text-transform: capitalize;">`;
            $("#states").append(tag);
        });
    }

}

window.addEventListener("load", () => {
    getStates();
})