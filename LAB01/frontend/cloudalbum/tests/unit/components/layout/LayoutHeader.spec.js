import { shallowMount } from '@vue/test-utils';
import LayoutHeader from '@/components/layout/LayoutHeader.vue';

describe('LayoutBody', () => {
  const wrapper = shallowMount(LayoutHeader);
  it('renders v-content', () => {
    expect(wrapper.find('v-app-bar-stub').exists()).toBe(true);
  });
});
