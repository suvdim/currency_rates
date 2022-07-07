<template>
  <div>
    <div
      :class="'mt-2 alert alert-' + message.type"
      role="alert"
      v-if="message.text"
    >
      {{ message.text }}
    </div>
    <div v-if="this.currencies.length">
      <p class="lead mt-4">Вы может выбрать одну или несколько валют и нажать на кнопку “Получить котировку”.</p>
      <h3 class="mt-3">Выберите валюту</h3>
      <ul class="list-unstyled">
        <li v-for="currency of currencies" :key="currency.id">
          <input
            class="form-check-input me-2"
            type="checkbox"
            :id="'currency-' + currency.id"
            :value="currency.code"
            v-model="checked"
          >
          <label
            class="form-check-label"
            :for="'currency-' + currency.id"
          >
            {{ currency.title }}
          </label>
        </li>
      </ul>
      <div class="mb-3">
        <button
          type="button"
          class="btn btn-success mx-1"
          @click.stop="submit"
        >
          {{ button_get_text }}
        </button>
        <button
          type="button"
          class="btn btn-link mx-1"
          @click.stop="toggle_checkboxes"
        >
          {{ button_check_text }}
        </button>
      </div>
    </div>
    <ExportButtons
      :rates="rates"
      :header="table_header"
      @notification="update_alert($event)"
    />
    <CurrencyTable
      :rates="rates"
      :header="table_header"
    />
  </div>
</template>

<script>
import axios from 'axios'
import CurrencyTable from '@/components/CurrencyTable'
import ExportButtons from '@/components/ExportButtons'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/'

export default {
  name: 'CurrenciesDashboard',
  components: {
    CurrencyTable,
    ExportButtons
  },
  data() {
    return {
      currencies: [],
      rates: [],
      checked: [],
      message: {
        text: false,
        type: 'success'
      },
      table_header: ["Код валюты", "Название валюты", "Цена", "Дата котировки", "Номинал"]
    };
  },
  computed: {
    button_get_text() {
      let text = 'Получить котировк'

      if (this.checked.length > 1) {
        return text + 'и'
      } else {
        return text + 'у'
      }
    },
    button_check_text() {
      if (this.checked.length) {
        return "Убрать выбранное"
      } else {
        return "Выбрать все валюты"
      }
    }
  },
  async created() {
    try {
      const res = await axios.get(`currencies/?format=json`)

      if (res.data.length) {
        this.currencies = res.data
      } else {
        this.update_alert('Извините, списка валют нет.', 'warning')
      }
    } catch (error) {
      console.log(error)
      this.update_alert('Извините, не удалось получить список валют.', 'danger')
    }
  },
  methods: {
    toggle_checkboxes() {
      let selected = []
      if (this.checked.length === 0) {
        this.currencies.forEach(function(currency) {
          selected.push(currency.code)
        })
      }
      this.checked = selected
    },
    update_alert(mtext, mtype='success') {
      if (!mtext) {
        return
      }
      this.message.text = mtext
      this.message.type = mtype
    },
    async submit() {
      this.message.text = false

      if (this.checked.length === 0) {
        this.update_alert('Выберите хотя бы одну валюту.', 'warning')
        return
      }
      const query = 'currency_code_latest__in=' + this.checked.join(',')

      try {
        const res = await axios.get(`rates/?${query}&format=json`)

        if (res.data.length) {
          this.rates = res.data
          this.update_alert('Таблица с курсами валют сформирована.')
        } else {
          this.update_alert('Извините, этих данных еще нет.', 'warning')
        }
      } catch (error) {
        console.log(error)
        this.update_alert('Извините, не удалось получить курсы валют.', 'danger')
      }
    }
  }
}
</script>
