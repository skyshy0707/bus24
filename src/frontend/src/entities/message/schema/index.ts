import type { Select } from "@shared/types/interfaces"

const MessageLabels: Record<string, string> = {
    atp_name: 'АТПравитель',
    text: 'Сообщение',
    date: 'Изменён'
}

const LeadLabels: Record<string, string> = {
    route_no: "Маршрут",
    route_wiki_url: "Источник"
}

const SelectLead: Select = {
    fieldName: "lead",
    selectType: "single"
}

const ATPLabels: Record<string, string> = {
    name: "АТП"
}

const SelectATP: Select = {
    fieldName: "to", // Имя поля в целевом объекте
    selectType: "multi"
}

export {
    ATPLabels,
    LeadLabels,
    MessageLabels,
    SelectATP, 
    SelectLead
}