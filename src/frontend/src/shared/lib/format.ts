const capitalize = (str: string) => str.charAt(0).toUpperCase() + str.slice(1)

const isEqual = (objA: object, objB: object) => {

    if (Object.keys(objA).length != Object.keys(objB).length){
        return false
    }
    for (let key of Object.keys(objA)){
        console.log(`a: ${objA[key]} b: ${objB[key]}`)
        if (objA[key] !== objB[key]){
            return false
        }
    }
    return true
}

function parseDate(datetime: string){
    const date = new Date(datetime)

    console.log(`date: ${date}, orr: ${datetime}`)
    //console.log(`object.date: ${this.object.date}, object.route_wiki_url: ${this.object.route_wiki_url}`)
    return date.toLocaleDateString() + '  ' + date.toLocaleTimeString().slice(0, 5)
}

export {
    capitalize, isEqual, parseDate
}