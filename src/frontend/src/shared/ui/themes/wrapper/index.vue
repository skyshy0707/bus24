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
    }

    @media (max-width: 460px){
        .wrapper {
            flex-direction : column;
        }
    }
</style>