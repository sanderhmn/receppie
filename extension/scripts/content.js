chrome.tabs.query({active: true, currentWindow: true}, tabs => {
    let url = tabs[0].url;

    //const dropdownEl = document.querySelector("#form")
    //const formData = new FormData(dropdownEl)
    //const time = formData.get('time')

    const myData = {
        url: url
    };

    const myOptions = {
        method: "POST", 
        body: JSON.stringify(myData),
    };

    const button = document.querySelector("#submit_btn");
    
    button.addEventListener("click", (event) => {
        fetch("http://127.0.0.1:5000/extension/add", myOptions)
            .then(console.log("Ok!"))
    })
});







