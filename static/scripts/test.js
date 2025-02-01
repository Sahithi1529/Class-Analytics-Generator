var view_data_btn = document.getElementById("view-data-btn");
var insert_data_btn = document.getElementById("insert-data-btn");
var download_data_btn = document.getElementById("download-data-btn");
function downloadData()
{
    
    console.log("HEEEEEEEEEEEEEEEE");
    resource = fetch('https://localhost:8000/administrator/download-data')
    var link = document.createElement('a');
    link.setAttribute('href','/static/users.csv')
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
}
function viewData()
{
console.log("Hello");
}
function insertData()
{
console.log("Hi");
}
view_data_btn.addEventListener('click',viewData);
insert_data_btn.addEventListener('click',insertData);
download_data_btn.addEventListener('click',downloadData);



