import mongoose from 'mongoose'


export const connectToDB = async ()=>{
    try {
        const DB_NAME = process.env.DB_NAME
        const MONGODB_URI = process.env.MONGODB_URI
        console.log(MONGODB_URI)


        if(!MONGODB_URI) throw new Error("MONGODB_URI is not defined"
        )
        
        const connection = await mongoose.connect(`${MONGODB_URI}`)
        const url = `${connection.connection.host}:${connection.connection.port}`
        if(connection) console.log(`MongoDB connected at ${url}`)
        return connection
    } catch (error) {
        console.log(error)
    }
}
