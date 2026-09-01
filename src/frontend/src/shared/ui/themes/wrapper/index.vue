<template>
    <div
        class="wrapper"
    >
        <slot>
        </slot>
    </div>
</template>

<style lang="css">
    .wrapper {
        display: flex;
        flex-direction: row;
        min-height: calc(100vh - 18px);
        align-items: stretch
    }

    @media (max-width: 460px){
        .wrapper {
            flex-direction : column;
            height: auto
        }
    }
</style>