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
        height: calc(100vh - 18px)
    }

    @media (max-width: 460px){
        .wrapper {
            flex-direction : column;
            height: auto
        }
    }
</style>