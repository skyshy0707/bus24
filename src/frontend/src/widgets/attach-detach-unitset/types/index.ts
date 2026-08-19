interface ChangeUnitSet {
    units: Array<number>,
    change_type: 'add' | 'remove'
}

type ModelControlPanelRequiredProps = 'crudModel' | 'object'

export type { ChangeUnitSet, ModelControlPanelRequiredProps }