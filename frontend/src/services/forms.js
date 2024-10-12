import axios from 'axios'

const baseUrl = 'http://127.0.0.1:5000/'

const getAll = () => {
    return (
        axios.get(baseUrl + 'players')
    )
}

export default {getAll}