const capitalize = (str: string) => str.charAt(0).toUpperCase() + str.slice(1)

const isEqual = (objA: object, objB: object) => {

    if (Object.keys(objA).length != Object.keys(objB).length){
        return false
    }
    for (let key of Object.keys(objA)){
        if (objA[key] !== objB[key]){
            return false
        }
    }
    return true
}

function parseDate(datetime: string){
    const date = new Date(datetime)
    return date.toLocaleDateString() + '  ' + date.toLocaleTimeString().slice(0, 5)
}

export {
    capitalize, isEqual, parseDate
}