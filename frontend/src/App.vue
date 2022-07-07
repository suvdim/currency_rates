<template>
  <PageHeader/>
  <main class="flex-shrink-0">
    <div class="container">
      <CurrenciesDashboard />
    </div>
  </main>
  <PageFooter/>
</template>

<script>
import CurrenciesDashboard from '@/components/CurrenciesDashboard'
import PageHeader from '@/components/PageHeader'
import PageFooter from '@/components/PageFooter'

export default {
  name: 'App',
  components: {
    CurrenciesDashboard,
    PageHeader,
    PageFooter
  }
}
</script>

<style>
#app {
  flex-direction: column!important;
  display: flex!important;
  min-height: 100vh!important;
}
</style>
