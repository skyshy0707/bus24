import type { AxiosResponse } from 'axios'

type CrudOpResult = any | string

interface DjangoErrorData {
  detail?: string;
  errors?: Record<string, string[]>; // Для ошибок валидации сериализатора
}

type Id = number | string

type SelectType = 'multi' | 'single'

interface Reactable<T> { value: T }

type Response = AxiosResponse<any>

type Item = {
    id: Id,
    atp_id?: Id
} & Record<string, any>

export type { 
  Id, 
  Item, 
  CrudOpResult, 
  DjangoErrorData,
  Reactable, 
  Response
}