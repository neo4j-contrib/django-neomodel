function myFunction() {
    var names = ["John", "Mike", "George"]
    for (var i = 0; i < names.length; i++) {
        var name = names[i];
        var li = document.createElement('li');
        li.innerHTML = name;
        document.getElementById('searchList').appendChild(li);
    }
    alert("Hello from a static file!");
}