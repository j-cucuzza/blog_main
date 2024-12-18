document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id") || "0"

    const htmxElement = document.querySelector("#get-recipe")
    if (htmxElement) {
        const endpoint = `https://www.dippingsauce.net/api/recipes/one/html?id=${encodeURIComponent(id)}`
        htmxElement.setAttribute("hx-get", endpoint)

        htmx.process(htmxElement)
    }
})


document.body.addEventListener("htmx:afterSwap", function(event) {
    const headers = event.detail.xhr.getAllResponseHeaders()
    const title = event.detail.xhr.getResponseHeader("x-page-title")
    const description = event.detail.xhr.getResponseHeader("x-page-description")

    if (title) {
        document.title = title + " | DIPPINGSAUCE"
    }

    let metaDescription = document.querySelector('meta[name="description"]')
    metaDescription.setAttribute("content", description)
})

const shareRecipe = (name) => {
    navigator.clipboard.writeText("Check out this recipe for " + name + ": " + window.location.href)
    document.getElementById('share-button').innerHTML = "Copied to Clipboard!";
}