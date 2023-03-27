function getRandom(arr, n) {
    var result = new Array(n),
        len = arr.length,
        taken = new Array(len)
        while (n--) {
            var x = Math.floor(Math.random() * len)
            result[n] = arr[x in taken ? taken[x] : x]
            taken[x] = --len in taken ? taken[len] : len
        }
    return result
}

var querySpan = document.getElementById("image-query");
//console.log("query=" + JSON.stringify(querySpan, undefined, 2));
var queryText = querySpan.textContent;
//console.log("textContent=" + queryText);
var query = queryText.replace(/ /g, '+');

var sites = [{
      name: "google",
      url: "https://www.google.com/search?tbm=isch&q=" + query + "clipart",
      selector: "a > div > img",
      amount: 3,
      random: true
   }
]

function scrapeImages(content, site) {

   let container = document.createElement("div")
   container.innerHTML = content
   let imageList = container.querySelectorAll(site.selector)
   let images = Array.from(imageList)

   let selected = (site.random ? getRandom(images.slice(0, 20), site.amount) : images.slice(0, site.amount))
   for (img of selected)  {
      img.parentNode.removeChild(img)
      document.getElementById(site.name + "-image").appendChild(img)
   }
}

function fetchHTML(site) {
   // pull content from page via API to avoid Same-origin policy
   fetch(`https://api.allorigins.win/get?url=${encodeURIComponent(site.url)}`)
      .then(response => {
         if (response.ok) return response.json()
         throw new Error('Network response was not ok.')
      })
      .then(data => scrapeImages(data.contents, site))
}

// Initiate search
for (site of sites) {
   fetchHTML(site)
}
