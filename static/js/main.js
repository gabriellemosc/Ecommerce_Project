
var url = new URL(document.URL);     //take the URL of our site 

var itens = document.getElementsByClassName("item-ordenar")

console.log(itens)

for(i=0; i < itens.length; i++){
    url.searchParams.set("ordem", itens[i].name);
    itens[i].href = url.href;
}



console.log(url)