const express = require("express")
const bodyParser = require("body-parser")

const app = express()
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.post("/webhook", (req, res) => {
    const from = req.body.From
    const msg = req.body.Body

    console.log(`Message from ${from}: ${msg}`)

    // Reply back to Twilio
    res.send(`<Response><Message>Hello! You said: ${msg}</Message></Response>`)
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => console.log(`Server running on port ${PORT}`))
