import type { CrudManager, CrudModel } from "@shared/types/interfaces"
import type { Id } from "@shared/types/types"

class Crud implements CrudManager {

    model: CrudModel

    constructor(model: CrudModel){
        this.model = model
    }

    setModel(model: CrudModel){
        this.model = model
    }

    async create(data: any){
        return await this.model.create(data)
    }

    async delete(id: Id){
        return await this.model.delete(id)
    }

    async edit(data: any, id: Id){
        return await this.model.edit(data, id)
    }

    async get(id: Id){
        return await this.model.get(id)
    }
}

export {
    Crud
}