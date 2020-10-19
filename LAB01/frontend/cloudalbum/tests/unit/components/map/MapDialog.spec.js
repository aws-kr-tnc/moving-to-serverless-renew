import { shallowMount } from '@vue/test-utils';
import MapDialog from '@/components/map/MapDialog.vue';

describe('MapDialog', () => {
  const wrapper = shallowMount(MapDialog);

  it('renders v-dialog', () => {
    expect(wrapper.find('v-dialog-stub').exists()).toBe(true);
  });
});
