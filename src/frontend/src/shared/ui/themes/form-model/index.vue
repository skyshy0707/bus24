<template>
    <slot></slot>
</template>

<style lang="css">
    .action-btn{
        margin: 4px;
        background-color: rgba(26, 1, 86, 0.6);
        border-radius: 15%;
        width: 90px
    }

    .apply-btn{
        margin: 4px;
        background-color: rgba(59, 58, 58, 0.6);
        border-radius: 15%;
        color: rgb(0, 27, 53);
        width: 90px
    }

    .form-model {
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        margin: 4px;
        padding: 0.2em 0;
        background-color: rgba(168, 141, 173, 0.6);
        border-radius: 10px
    }

    .model {
        padding-bottom: 0.5em;
        flex-direction: column
    }

    .model > div {
        padding-bottom: 0.5em
    }

    .model > div > div {
        padding-bottom: 0.5em;
        width: 220px
    }
</style>