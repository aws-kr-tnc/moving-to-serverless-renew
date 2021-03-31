import { shallowMount } from '@vue/test-utils';
import LayoutFooter from '@/components/layout/LayoutFooter.vue';

describe('LayoutBody', () => {
  const wrapper = shallowMount(LayoutFooter);
  it('renders v-footer', () => {
    expect(wrapper.find('v-footer-stub').exists()).toBe(true);
  });
});
