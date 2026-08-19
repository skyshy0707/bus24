import { request }  from  "@shared/api/schema/requests"

import type { ChangeUnitSetParams } from "features/attach-detach-unitset-btn/types"


async function changeLeadUnitSet(id: number, data: ChangeUnitSetParams){
    const response = await request({
        url: `lead/${id}/unit-set/modify`,
        data: data,
        method: 'PATCH'
    })
    return response.status === 200 ? response.data : response
}

export { changeLeadUnitSet }