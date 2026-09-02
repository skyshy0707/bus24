<template>

    <div class="sidebar">
        <button
            @click="() => to('/profile')"
            role="button"
            class="sidebar-btn"
        >
            Profile
        </button>
        <button
            @click="() => to('/')"
            role="button"
            class="sidebar-btn"
        > 
            Dashboard
        </button>
    </div>


</template>

<style lang="css">
    .sidebar {
        align-items: self-start;
        display: flex;
        flex: 0 0 120px;
        flex-direction: column;
        flex-shrink: 0;
        margin-right: 2em;
        background-image: linear-gradient(to top, rgb(141, 119, 148), #280049a2, rgb(28, 0, 46));
        height: auto;
        min-height: 100vh;
        position: fixed;
        overflow-y: auto;
    }

    .sidebar-btn{
        background-color:#273b00a6;
        color: white;
        border-radius : 6px;
        height: 1.5rem;
        width: 93%;
        margin: 0.5em;
        padding: 6px;
        text-align: center;
        justify-content: center;
        display: inline-flex;
        align-items: center
    }

    @media (max-width: 460px) {
        .sidebar {
            flex-direction: row;
            flex: 0 0 100%;
            min-height: auto;
            min-width: 100vw
        }
        .sidebar-btn{
            width: 100%;
        }
    }


</style>

<script setup>

    import styles from 'features/sidebar/ui/element/styles.module.css'
    import { to } from '@shared/api/schema/requests'

</script>

<style
    lang="css"
    :module="styles"
>
</style>