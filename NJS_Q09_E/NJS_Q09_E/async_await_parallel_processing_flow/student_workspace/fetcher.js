// TODO: Refactor fetchUrls to execute the promises in parallel using Promise.all
// rather than waiting sequentially in a loop, returning the results array.
async function fetchUrls(urls) {
    const results = [];
    for (const url of urls) {
        const res = await fakeFetch(url);
        results.push(res);
    }
    return results;
}

function fakeFetch(url) {
    return new Promise(resolve => setTimeout(() => resolve(`Data from ${url}`), 100));
}

module.exports = { fetchUrls };
