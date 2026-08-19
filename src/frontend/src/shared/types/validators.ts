const actionType = (value: string) => {
    return ["create", "edit", "view"].includes(value)
}

export {
    actionType
}