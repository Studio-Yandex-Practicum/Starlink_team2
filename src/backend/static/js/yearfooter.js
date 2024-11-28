const startYear = 2024;
const currentYear = new Date().getFullYear();
let yearText = startYear;
if(currentYear > startYear) {
    yearText += '-' + currentYear;
}
document.getElementById("currentYear").innerHTML = yearText;