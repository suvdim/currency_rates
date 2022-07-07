<template>
  <div
    v-if="rates.length"
    class="d-grid gap-2 d-md-flex justify-content-md-end"
  >
    <span class="pt-1">Экспортировать курсы валют</span>
    <button
      type="button"
      class="btn btn-primary btn-sm"
      @click.stop="excel_csv_button('csv')"
    >
      CSV
    </button>
    <button
      type="button"
      class="btn btn-primary btn-sm"
      @click.stop="excel_csv_button"
    >
      Excel
    </button>
    <button
      type="button"
      class="btn btn-primary btn-sm"
      @click.stop="pdf_button"
    >
      PDF
    </button>
  </div>
</template>

<script>
import * as XLSX from 'xlsx/xlsx.mjs'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

require('@/assets/fonts/NotoSans-Regular-normal')

export default {
  name: 'ExportButtons',
  props: {
    rates: {
      type: Array,
      required: true
    },
    header: {
      type: Array,
      required: true
    }
  },
  methods: {
    excel_csv_button(file_type='excel') {
      const data = XLSX.utils.json_to_sheet(this.rates)
      const wb = XLSX.utils.book_new()

      // get max width for currency_title column
      const max_title_width = this.rates.reduce((w, r) => Math.max(w, r.currency_title.length), 16)
      // set columns width in characters
      data["!cols"] = [
        {wch: 11},
        {wch: max_title_width},
        {wch: 10},
        {wch: 17},
        {wch: 8},
      ]

      XLSX.utils.book_append_sheet(wb, data, 'Курсы Валют')
      XLSX.utils.sheet_add_aoa(data, [this.header], { origin: "A1" })

      // return the file
      if (file_type === 'csv') {
        XLSX.writeFile(wb, 'currencies-csv.csv', {bookType:"csv", FS:";"})
        this.$emit('notification', 'CSV файл сформирован.')
      } else {
        XLSX.writeFile(wb, 'currencies-excel.xlsx')
        this.$emit('notification', 'Excel файл сформирован.')
      }
    },
    pdf_button() {
      const doc = new jsPDF()
      // workaround for utf-8
      doc.setFont('NotoSans-Regular', 'normal')

      // prepare the data
      const data = this.rates.map(i => Object.keys(i).map(j => i[j]))

      autoTable(doc, {
        head: [this.header],
        body: data,
        headStyles: {
          fillColor: 'fff',
          fontStyle: 'bold',
          textColor: '000',
          lineWidth: [0, 0, 0.5, 0],
          lineColor: '000'
        },
        bodyStyles: {
          lineWidth: [0, 0, 0.2, 0],
        },
        styles: {
          font: 'NotoSans-Regular',
          fontStyle: 'normal'
        }
      })

      // return the file
      doc.save('currencies-pdf.pdf')
      this.$emit('notification', 'PDF файл сформирован.')
    }
  }
}
</script>
