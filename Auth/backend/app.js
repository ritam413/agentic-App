import express from 'express'
import cors from 'cors'
import cookieParser from 'cookie-parser'

const app = express()

app.use(cors({
  origin: "http://localhost:5173",
  credentials: true
}));

app.use(cookieParser())
app.use(express.json())
app.use(express.urlencoded({extended: true}))
app.use(express.static('public'))


//import routes
import userAuthRoutes from './routes/userAuth.routes.js'

app.use("/api/auth/",userAuthRoutes)

export {app}