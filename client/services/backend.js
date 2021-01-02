import cookie from 'react-cookies'

const Backend = {
    get(url) {
        return fetch(url, {
            method: 'GET',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": cookie.load('csrftoken'),
            },
        }).then(response => {
            return response.json()
        })
    },

    post(url, data, contentType="application/json") {
        let body = data
        let headers = {
            "Content-Type": contentType,
            "X-CSRFToken": cookie.load('csrftoken'),
        }

        if (contentType == "application/json") {
            body = JSON.stringify(data)
        } else if (contentType == "application/csv") {
            headers["Content-Disposition"] = "attachment; filename=file.csv"
        }

        return fetch(url, {
            method: 'POST',
            body: body,
            credentials: 'include',
            headers: headers,
        }).then(results => {
            return results.json()
        })
    },
}

export default Backend
