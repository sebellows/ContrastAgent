<script>
import { includes } from '@/utils/includes';
import ToggleBase from './_ToggleBase';

export default {
  name: 'mico-checkbox',

  inject: {
    toggleGroup: {
      from: 'MicoCheckboxGroup',
      default: function () {
        return this;
      },
    },
  },

  props: {
    checked: {
      type: Boolean,
      default: false,
    },
    inline: {
      type: Boolean,
      default: false,
    },
    labelClass: {
      type: [String, Array, Object] as PropType<null | string | string[] | Record<string, boolean>>,
      default: null,
    },
    pretty: {
      type: Boolean,
      default: false,
    },
    value: {
      type: [Boolean, Number, String, Object],
      default: true,
    },
    indeterminate: {
      type: Boolean,
      default: false,
    },
    // Custom switch styling
    switch: {
      type: Boolean,
      default: false,
    },
  },

  setup({ props }) {
    const inputRef = ref<HTMLInputElement | null>(null)
    const isChecked = ref<boolean>(!!props.checked)
    const buttons = ref<boolean>(!!props.buttons)
    const hasFocus = ref<boolean>(false)
    const localChecked = ref<boolean | null>(null)

    const isChecked = computed(() => {
      const checked = this.inputRef.value?.$el?.checked
      const value = this.value;

      if (Array.isArray(checked)) {
        return includes(checked, value, null, true) > -1;
      }

      return checked == value;
    })

    watch(() => {
      computedLocalChecked(newVal, oldVal) {
        this.$emit('input', newVal);

        if (this.$refs && this.$refs.input) {
          this.$emit('update:indeterminate', this.$refs.input.indeterminate);
        }
      },
      indeterminate(newVal, oldVal) {
        this.setIndeterminate(newVal);
      },
    })

    mounted() {
      // Set initial indeterminate state
      this.setIndeterminate(this.indeterminate);
    },

    const handleChange = ({ target: { checked, indeterminate } }) => {
      localChecked.value = checked
      const value = this.value;
      let uncheckedValue = null;

      // Update computedLocalChecked
      if (Array.isArray(localChecked)) {
        console.log('Checkbox: localChecked', localChecked);
        const idx = localChecked.indexOf(value);

        if (checked && idx < 0) {
          // add value to array
          localChecked = localChecked.concat(value);
        } else if (!checked && idx > -1) {
          // remove value from array
          localChecked = localChecked.slice(0, idx).concat(localChecked.slice(idx + 1));
        }
      } else {
        uncheckedValue = this.uncheckedValue;
        localChecked = checked ? value : uncheckedValue;
      }
      this.computedLocalChecked = localChecked;

      // Change is only emitted on user interaction
      this.$emit('change', checked ? value : uncheckedValue);

      // If this is a child of form-checkbox-group, we emit a change event on it as well
      if (this.isGroup) {
        this.toggleGroup.$emit('change', localChecked);
      }

      this.$emit('update:indeterminate', indeterminate);
    }

    const setIndeterminate = (state) => {
      // Indeterminate only supported in single checkbox mode
      if (Array.isArray(this.computedLocalChecked)) {
        state = false;
      }
      if (this.$refs && this.$refs.input) {
        this.$refs.input.indeterminate = state;
        // Emit update event to prop
        this.$emit('update:indeterminate', state);
      }
    }
  }
};
</script>
