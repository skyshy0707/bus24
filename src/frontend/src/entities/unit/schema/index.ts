import type { Select } from "@shared/types/interfaces"

const UnitColorLabels: Record<string, string> = {
    "value": "Название"
}

const BusLabels: Record<string, string> = {
    "model": "Модель",
    "capacity": "Вместимость"
}

const SelectBus: Select = {
    fieldName: "bus_id",
    selectType: "single"
}

const SelectUnitColor: Select = {
    fieldName: "color",
    selectType: "single"
}

export {
    BusLabels,
    UnitColorLabels,
    SelectBus,
    SelectUnitColor
}