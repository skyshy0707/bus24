import type { Select } from "@shared/types/interfaces"

const BusCathegoryLabels: Record<string, string> = {
    "value": "Значение"
}

const SelectBusCathegory: Select = {
    fieldName: "capacity_class",
    selectType: "single"
}

export {
    BusCathegoryLabels,
    SelectBusCathegory
}