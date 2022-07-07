<template>
  <table
      class="table table-hover table-striped mt-3 mb-5"
      v-if="rates.length"
  >
    <thead>
    <tr>
      <th scope="col" v-for="title of header" :key="title">
        {{ title }}
      </th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="rate of rates" :key="rate.id">
      <td>{{ rate.currency_code }}</td>
      <td>{{ rate.currency_title }}</td>
      <td>{{ rate.value }}</td>
      <td>{{ rate.value_date }}</td>
      <td>{{ rate.nominal }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'CurrencyTable',
  props: {
    rates: {
      type: Array,
      required: true
    },
    header: {
      type: Array,
      required: true
    }
  }
}
</script>
