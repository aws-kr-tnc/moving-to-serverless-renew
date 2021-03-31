import { shallowMount } from '@vue/test-utils';
import App from '@/App.vue';

describe('App', () => {
  const wrapper = shallowMount(App);

  it('renders the component', () => {
    expect(wrapper.html()).toMatchSnapshot();
  });

  it('renders layout-header', () => {
    expect(wrapper.find('layout-header-stub').exists()).toBe(true);
  });

  it('renders layout-body', () => {
    expect(wrapper.find('layout-body-stub').exists()).toBe(true);
  });

  it('renders layout-footer', () => {
    expect(wrapper.find('layout-footer-stub').exists()).toBe(true);
  });
});
