<script>
import Checkbox from './Checkbox';
import ToggleGroupBase from './_ToggleGroupBase';

export default {
    name: 'mico-checkbox-group',

    components: { Checkbox },

    extends: ToggleGroupBase,

    provide() {
        return {
            micoCheckboxGroup: this,
        };
    },

    props: {
        // Custom switch styling
        switches: {
            type: Boolean,
            default: false,
        },
    },

    data() {
        return {
            localChecked: this.checked,
        };
    },

    computed: {
        isRadioGroup() {
            return false;
        },
    },
};
</script>
