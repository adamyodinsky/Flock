import axios, { CanceledError } from "axios";


export default axios.create({
  // baseURL: process.env.REACT_APP_BASE_URL,
  baseURL: "http://localhost/",
})

export { CanceledError };
