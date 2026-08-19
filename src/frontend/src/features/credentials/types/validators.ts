const actionType = (value: string) => {
    return ["signin", "signup"].includes(value)
}

export {
    actionType
}